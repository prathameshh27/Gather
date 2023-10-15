from ..serializers.meeting_serializer import MeetingSerializer, Meeting
from django.db.models import Q

from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from django.contrib.auth.decorators import login_required

from apps.lib.utils.functions import (
    resp_excp_handler,
    get_validation_errors,
    )

# ToDo: Minimize the use of conditional blocks. 
# Add validations at serializer level instead.

class MeetingViewSet:

    RESPONSE = {"message": "Something went wrong. The request could not be fulfilled"}
    HTTP_STATUS = 500


    # create a meeting
    @resp_excp_handler
    def create_meeting(self, request) -> Response:
        response = self.RESPONSE
        http_status = self.HTTP_STATUS

        post_data = request.data
        post_data["created_by"] = request.user.get_id()
        
        meeting_serializer = MeetingSerializer(data=post_data, many=False)

        if meeting_serializer.is_valid():
            meeting = meeting_serializer.save()
            response = {
                "id" : meeting.id,
                "unavailable_users" : {
                    "users" : meeting.unavailable_users,
                    "message" : "Some users might not be added due to scheduling conflict"
                }
            }
            http_status = 201
        else:
            response = {"message" : "meeting could not be added"}
            response["errors"]  = get_validation_errors(meeting_serializer)
        return Response(data=response, status=http_status)

    # list all meetings
    @resp_excp_handler
    def list_meetings(self, request) -> Response:
        response = self.RESPONSE
        http_status = self.HTTP_STATUS

        # queryparams = {}
        # queryparams["starts_at__gte"] = "2023-10-12T22:20"
        # queryparams["ends_at__lte"] = "2023-10-12T23:35"

        start_date = "2023-10-15T17:00:00+05:30"
        end_date   = "2023-10-15T17:30:00+05:30"

        start_date = "2023-10-15T17:30:00+05:30"
        end_date   = "2023-10-15T18:00:00+05:30"

        start_date = "2023-10-15T15:30:00+05:30"
        end_date   = "2023-10-15T17:40:00+05:30"

        queryparams = (
        (Q(starts_at__gte=start_date) & Q(starts_at__lt=end_date)) |
        (Q(ends_at__gt=start_date) & Q(ends_at__lte=end_date))
        )

        # queryparams = ()

        # queryparams = (
        # Q(starts_at__range=(start_date, end_date)) 
        # | Q(ends_at__range=(start_date, end_date))
        # )

        # meetings = Meeting.list_meetings(queryparams)
        meetings = Meeting.list_meetings()
        meeting_serializer = MeetingSerializer(meetings, many=True)
        response = meeting_serializer.data
        http_status = 200
        
        return Response(response, status=http_status)

    # describe meeting
    @resp_excp_handler
    def describe_meeting(self, request) -> Response:
        response = self.RESPONSE
        http_status = self.HTTP_STATUS

        req = request.data
        meeting_id = req.get("id", None)
        if meeting_id:
            meeting = Meeting.get_meeting(id=meeting_id)
            if meeting:
                meeting_serializer = MeetingSerializer(meeting, many=False)
                response = meeting_serializer.data
                http_status = 200
            else:
                response = {"message" : "No meeting found with the supplied id: {}.".format(meeting_id) }
                http_status = 200
        else:
            response = {"message" : "Please supply a valid 'id' via the request"}
            http_status = 400
        return Response(response, status=http_status)

    # update meeting
    @resp_excp_handler
    def update_meeting(self, request) -> Response:
        response = self.RESPONSE
        http_status = self.HTTP_STATUS

        post_data = request.data
        # post_data["created_by"] = request.user.get_id()
        meeting_id = post_data.get("id", None)

        if meeting_id:
            meeting = Meeting.get_meeting(meeting_id)
            if meeting:
                meeting_serializer = MeetingSerializer(instance=meeting, data=post_data)
                if meeting_serializer.is_valid():
                    meeting_serializer.save()
                    response, http_status = meeting_serializer.data, 200

                    response["unavailable_users"] = {
                        "users" : meeting_serializer.validated_data.get("unavailable_users", []),
                        "message" : "Some users might not be added due to scheduling conflict"
                    }
                else:
                    response = {"message" : "meeting could not be updated"}
                    response["errors"]  = get_validation_errors(meeting_serializer)
            else:
                response = {"message" : "meeting not found"}
        else:
            response = {"message" : "Please supply a valid meeting 'id' via the request"}
        
        return Response(data=response, status=http_status)
    

    # ToDo: optimize the fuction and reduce conditional blocks
    @resp_excp_handler
    def manage_users(self, request):
        response = self.RESPONSE
        http_status = self.HTTP_STATUS

        req = request.data
        meeting_id = req.get("id", "9999")
        attendees = req.get("attendees", [])
        operation = req.get("operation", None)

        meeting = Meeting.get_meeting(id=meeting_id)
        if meeting:
            if all([attendees, operation]):
                if operation == "add":
                    success = meeting.add_attendees(attendees)
                    if success:
                        response, http_status = {"message" : "Attendees added successfully"}, 201
                    else:
                        response, http_status = {"message" : "Error! Attendees could not be added"}, 400
                elif operation == "remove":
                    success = meeting.remove_attendees(attendees)
                    if success:
                        response, http_status = {"message" : "Attendees removed successfully"}, 201
                    else:
                        response, http_status = {"message" : "Error! Attendees could not be removed"}, 400
                else:
                    response, http_status = {"message" : "Invalid operation! Use 'add' or 'removed'"}, 400
            else:
                response, http_status = {"message" : "Invalid parameters supplied."}, 400
                response["example"] = {
                    "id" : "<int>",
                    "attendees" : ["<username.1:str>","<username.2:str>"],
                    "operation" : "add | remove"
                }
        else:
            response = {"message" : "Please supply a valid 'id' via the request"}
            http_status = 400

        return Response(response, status=http_status)



    @resp_excp_handler
    def delete_meeting(self, request):
        response = self.RESPONSE
        http_status = self.HTTP_STATUS

        req = request.data
        meeting_id = req.get("id", None)
        if meeting_id:
            is_success = Meeting.delete_meeting(id=meeting_id)
            if is_success:
                response = {"message" : "Meeting deleted"}
                http_status = 202 #accepted
            else:
                response = {"message" : "Error occured while deleting the meeting"}
                http_status = 400
        else:
            response = {"message" : "Please supply a valid 'id' via the request"}
            http_status = 400

        return Response(response, status=http_status)