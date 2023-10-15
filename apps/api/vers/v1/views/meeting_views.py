from apps.api.vers.v1.viewsets.meeting_viewset import MeetingViewSet
from rest_framework.decorators import api_view

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

meeting = MeetingViewSet()

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_meeting(request: object) -> object:
    response = meeting.create_meeting(request)
    return response


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_meetings(request: object) -> object:
    response = meeting.list_meetings(request)
    return response


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def describe_meeting(request: object) -> object:
    response = meeting.describe_meeting(request)
    return response


@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_meeting(request: object) -> object:
    response = meeting.update_meeting(request)
    return response


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def manage_users(request:object) -> object:
    response = meeting.manage_users(request)
    return response


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_meeting(request:object) -> object:
    response = meeting.delete_meeting(request)
    return response

