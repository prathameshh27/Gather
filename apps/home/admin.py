from django.contrib import admin

from .models.user import CustomUser
from .models.meeting import Meeting

# Register your models here.

class AdminUser(admin.ModelAdmin):
    list_display = ['id','username', 'date_joined', 'last_login', 'is_superuser']

class AdminMeeting(admin.ModelAdmin):
    list_display = ["id", "title", "description", "created_by", "starts_at", "ends_at"]


admin.site.register(CustomUser, AdminUser)
admin.site.register(Meeting, AdminMeeting)