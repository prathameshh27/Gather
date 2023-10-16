from django.urls import path, include
from .views.views import index

# Root level urls for switching between diffrent implementations of APIs

urlpatterns = [
    path('', index),
    path('v1/', include("apps.api.vers.v1.urls"))
  # path('v2/', include("apps.api.vers.v2.urls"))        # example
]
