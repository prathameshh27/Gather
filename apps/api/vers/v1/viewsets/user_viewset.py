from rest_framework.response import Response
from ..serializers.user_serializer import UserSerializer, CustomUser
# from ..serializers.meeting_serializer import meetingSerializer
from apps.lib.utils.functions import (
    resp_excp_handler,
    get_validation_errors,
    )

# ToDo: Minimize the use of conditional blocks. 
# Add validations at serializer level instead.

class UserViewSet:

    RESPONSE = {"message": "Something went wrong. The request could not be fulfilled"}
    HTTP_STATUS = 500

    @resp_excp_handler
    def index(self, request):
        response = self.RESPONSE
        http_status = self.HTTP_STATUS

        message = {
            "message": "You have accessed an API V1 resource"
            }
        return Response(data=message)
    
    @resp_excp_handler
    def unauthorized_api(self, request):
        requested_url = request.GET.get("next", request.path)
        resp = {
                    "url" : requested_url,
                    "msg" : "you are not logged in"
                }

        return Response(resp, safe=False)

    # create a user
    @resp_excp_handler
    def create_user(self, request) -> Response:
        response = self.RESPONSE
        http_status = self.HTTP_STATUS

        post_data = request.data
        is_list = True if isinstance(post_data, list) else False
        
        user_serializer = UserSerializer(data=post_data, many=is_list)

        if user_serializer.is_valid():
            user = user_serializer.save()

            user_list = user if isinstance(user, list) else [user]
            user_ids = [user.id for user in user_list]

            response = {
                "id" : str(user_ids)
            }
            http_status = 201
        else:
            response = {"message" : "User could not be added"}
            response["errors"]  = get_validation_errors(user_serializer)

        return Response(data=response, status=http_status)

    # list all users
    @resp_excp_handler
    def list_users(self, request) -> Response:
        response = self.RESPONSE
        http_status = self.HTTP_STATUS

        users = CustomUser.list_users()
        user_serializer = UserSerializer(users, many=True)
        response = user_serializer.data
        http_status = 200
        
        return Response(response, status=http_status)

    # describe user
    @resp_excp_handler
    def describe_user(self, request) -> Response:
        response = self.RESPONSE
        http_status = self.HTTP_STATUS

        req = request.data
        user_id = req.get("id", None)
        if user_id:
            user = CustomUser.get_user(id=user_id)
            if user:
                user_serializer = UserSerializer(user, many=False)
                response = user_serializer.data
                http_status = 200
            else:
                response = {"message" : "No user found with the supplied id: {}.".format(user_id) }
                http_status = 200
        else:
            response = {"message" : "Please supply a valid 'id' via the request"}
            http_status = 400
        return Response(response, status=http_status)

    # update user
    @resp_excp_handler
    def update_user(self, request) -> Response:
        response = self.RESPONSE
        http_status = self.HTTP_STATUS

        post_data = request.data
        user_id = post_data.get("id", None)

        if user_id:
            user = CustomUser.get_user(user_id)
            if user:
                user_serializer = UserSerializer(instance=user, data=post_data)
                
                if user_serializer.is_valid():
                    user_serializer.save()
                    response, http_status = user_serializer.data, 200                     
                
                else:
                    response = {"message" : "User could not be updated"}
                    response["errors"]  = get_validation_errors(user_serializer)
            else:
                response = {"message" : "User not found"}
        else:
            response = {"message" : "Please supply a valid user 'id' via the request"}
        
        return Response(data=response, status=http_status)
    
    # @resp_excp_handler
    # def get_user_meetings(self, request) -> Response:
    #     response = self.RESPONSE
    #     http_status = self.HTTP_STATUS

    #     req = request.data
        
    #     user_id = req.get("id", None)
    #     if user_id:
    #         user = CustomUser.get_user(user_id)
    #         if user:
    #             meetings = user.get_meetings()
    #             meeting_serializer = meetingSerializer(meetings, many=True)
    #             response = meeting_serializer.data
    #             http_status = 200
    #         else:
    #             response = {"message" : "No user found with the supplied id: {}.".format(user_id) }
    #             http_status = 200
    #     else:
    #         response = {"message" : "Please supply a valid 'id' via the request"}
    #         http_status = 400
    #     return Response(response, status=http_status)

