from rest_framework.response import Response

from ..serializers.meeting_serializer import MeetingSerializer, Meeting
from apps.lib.utils.functions import resp_excp_handler, get_validation_errors

# created a class for future extesibility
class MeetingViewSet:
    """Supports All the functions based meeting views."""

    RESPONSE = {"message": "Something went wrong. The request could not be fulfilled"}
    HTTP_STATUS = 500

    # create a meeting
    @resp_excp_handler
    def create_meeting(self, request) -> Response:
        """Creates a user object based on the request payload"""
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
        """Lists all existing meetings the user is added to"""
        response = self.RESPONSE
        http_status = self.HTTP_STATUS

        logged_user = request.user

        # SuperUsers can view all the meetings
        if logged_user.is_superuser:
            meetings = Meeting.list_meetings()
        else:
            meetings = logged_user.list_meetings()

        meeting_serializer = MeetingSerializer(meetings, many=True)
        response = meeting_serializer.data
        http_status = 200

        return Response(response, status=http_status)


    # describe meeting
    @resp_excp_handler
    def describe_meeting(self, request) -> Response:
        """Describes a meeting based on the supplied meeting id"""
        response = self.RESPONSE
        http_status = self.HTTP_STATUS

        logged_user = request.user
        req = request.data

        meeting_id = req.get("id", None)
        if meeting_id:

            if logged_user.is_superuser:
                meeting = Meeting.get_meeting(id=meeting_id)
            else:
                queryset = {'id': meeting_id}
                meeting = logged_user.list_meetings(queryset)
                meeting = meeting[0] if meeting.count() > 0 else None

            if meeting:
                meeting_serializer = MeetingSerializer(meeting, many=False)
                response = meeting_serializer.data
                http_status = 200
            else:
                response = {"message" : f"No meeting found with the supplied id: {meeting_id}." }
                http_status = 200
        else:
            response = {"message" : "Please supply a valid 'id' via the request"}
            http_status = 400
        return Response(response, status=http_status)


    # update meeting
    @resp_excp_handler
    def update_meeting(self, request) -> Response:
        """Updates an existing meeting based on the supplied payload"""
        response = self.RESPONSE
        http_status = self.HTTP_STATUS

        logged_user = request.user
        post_data = request.data
        meeting_id = post_data.get("id", None)

        if meeting_id:
            meeting = Meeting.get_meeting(meeting_id)

            if meeting:
                # Returns unauthorized code if the logged in user is not the owner of the meeting
                if logged_user != meeting.created_by:
                    response, http_status = {"message" : "You are not authorized to update this meeting"}, 403
                    return Response(data=response, status=http_status)

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
    def manage_users(self, request) -> Response:
        """Lets the user add or remove attendees from the meeting"""
        response = self.RESPONSE
        http_status = self.HTTP_STATUS

        logged_user = request.user
        req = request.data

        meeting_id = req.get("id", "9999")
        attendees = req.get("attendees", [])
        operation = req.get("operation", None)

        meeting = Meeting.get_meeting(id=meeting_id)
        if meeting:

            # Returns unauthorized code if the logged in user is not the owner of the meeting
            if logged_user != meeting.created_by:
                response, http_status = {"message" : "You are not authorized to update this meeting"}, 403
                return Response(data=response, status=http_status)

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
        """Deletes meeting only if the logged user owns it"""
        response = self.RESPONSE
        http_status = self.HTTP_STATUS

        logged_user = request.user
        req = request.data

        meeting_id = req.get("id", "0!")

        # Returns unauthorized code if the logged in user is not the owner of the meeting
        meeting = Meeting.get_meeting(id=meeting_id)

        if meeting:
            if logged_user != meeting.created_by:
                response, http_status = {"message" : "You are not authorized to update this meeting"}, 403
                return Response(data=response, status=http_status)

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
    