from django.contrib import admin
from django.urls import path
from .views.user_views import *
from .views.meeting_views import *

urlpatterns = [
    path('', index, name='list_users'),
    path('unauthorized', unauthorized_api, name='unauthorized_api'),

    #User 
    path('user/create', create_user, name='create_user'),
    path('user/update', update_user, name='update_user'),
    path('user/describe', describe_user, name='describe_user'),
    path('user/list', list_users, name='list_users'),

    #Meeting
    path('meeting/create', create_meeting, name='create_meeting'),
    path('meeting/update', update_meeting, name='update_meeting'),
    path('meeting/manage_users', manage_users, name='manage_users'),
    path('meeting/describe', describe_meeting, name='describe_meeting'),
    path('meeting/list', list_meetings, name='list_meetings'),
    path('meeting/delete', delete_meeting, name='delete_meeting'),
]
