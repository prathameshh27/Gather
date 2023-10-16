from rest_framework.response import Response
from ..serializers.user_serializer import UserSerializer, CustomUser
from apps.lib.utils.functions import resp_excp_handler, get_validation_errors


# created a class for future extesibility
class UserViewSet:
    """Supports All the functions based user views."""

    RESPONSE = {"message": "Something went wrong. The request could not be fulfilled"}
    HTTP_STATUS = 500

    @resp_excp_handler
    def index(self, request):
        """use for testing purpose"""
        message = {
            "message": "You have accessed an API V1 resource"
            }
        return Response(data=message)

    @resp_excp_handler
    def unauthorized_api(self, request):
        """Failed login attempts will be redirected to this view"""
        requested_url = request.GET.get("next", request.path)
        resp = {
                    "url" : requested_url,
                    "msg" : "you are not logged in"
                }
        return Response(resp)


    # create a user
    @resp_excp_handler
    def create_user(self, request) -> Response:
        """Creates user object based on the request payload"""
        response = self.RESPONSE
        http_status = self.HTTP_STATUS

        post_data = request.data
        is_list = True if isinstance(post_data, list) else False
        
        user_serializer = UserSerializer(data=post_data, many=is_list)

        if user_serializer.is_valid():
            user = user_serializer.save()

            # The fuction accepts multiple users in the payload
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
        """list all the users"""
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
        """Describe a user supplied through the payload"""
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
                response = {"message" : f"No user found with the supplied id: {user_id}." }
                http_status = 200
        else:
            response = {"message" : "Please supply a valid 'id' via the request"}
            http_status = 400
        return Response(response, status=http_status)


    # update user
    @resp_excp_handler
    def update_user(self, request) -> Response:
        """Update an existing user with the supplied payload"""
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
