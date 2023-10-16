from rest_framework.decorators import authentication_classes, permission_classes, api_view

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from apps.lib.utils.functions import superuser_required
from apps.api.vers.v1.viewsets.user_viewset import UserViewSet


user = UserViewSet()


@api_view(['GET'])
@superuser_required
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def index(request):
    """index"""
    response = user.index(request)
    return response


@api_view(['GET'])
@superuser_required
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def unauthorized_api(request):
    """unauthorized_api"""
    response = user.unauthorized_api(request)
    return response


@api_view(['POST'])
@superuser_required
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_user(request: object) -> object:
    """create_user"""
    response = user.create_user(request)
    return response


@api_view(['GET'])
@superuser_required
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_users(request: object) -> object:
    """list_users"""
    response = user.list_users(request)
    return response


@api_view(['GET'])
@superuser_required
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def describe_user(request: object) -> object:
    """describe_user"""
    response = user.describe_user(request)
    return response


@api_view(['PATCH'])
@superuser_required
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_user(request: object) -> object:
    """update_user"""
    response = user.update_user(request)
    return response
