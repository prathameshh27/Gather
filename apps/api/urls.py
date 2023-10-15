from django.contrib import admin
from django.urls import path, include
from .views.views import index

urlpatterns = [
    path('', index),
    path('v1/', include("apps.api.vers.v1.urls"))
]
