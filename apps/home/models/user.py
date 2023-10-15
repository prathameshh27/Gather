from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.lib.utils.functions import custom_id
from django.utils import timezone
from django.db.models import Q
from django.conf import settings

class CustomUser(AbstractUser):
    
    IST_TZ = settings.IST_TZ

    id = models.CharField(primary_key=True, unique=True, editable=False, default=custom_id, max_length=11)

    # returns name and id both for debugging purpose 
    def __str__(self) -> str:
        return "{}".format(self.username)

    def get_id(self) -> str:
        """Get user ID"""
        return self.id
    
    def get_obj(self) -> object:
        """Get user object"""
        return self


    def list_meetings(self, queryset={}) -> str:
        """List all the meeting where the current user is an attendee"""
        return self.meeting_attendee.filter(**queryset)


    def list_upcoming_meetings(self):
        """List all the upcoming meeting where the current user is an attendee"""
        now = timezone.now().astimezone(self.IST_TZ)
        return self.meeting_attendee.filter(starts_at__gte = str(now))


    def list_managed_meetings(self, queryset={}) -> str:
        """Get user ID"""
        return self.meeting_owner.filter(**queryset)
        

    def check_schedule_conflict(self, starts_at, ends_at) -> bool:    
        """Checks if the user has a conflicting schedule while setting up a new meeting"""
        try:
            upcoming_meetings = self.list_upcoming_meetings()
            
            queryparams = (
                (Q(starts_at__gte=starts_at) & Q(starts_at__lt=ends_at)) |
                (Q(ends_at__gt=starts_at) & Q(ends_at__lte=ends_at))
            )
            meetings = upcoming_meetings.filter(queryparams)

            is_available = False if meetings.count() > 0 else True
        
        except Exception as exp:
            is_available = None
        
        return is_available
  
    
    @classmethod
    def list_users(cls) -> object:
        """List all users"""
        return cls.objects.all()
    
    @classmethod
    def get_user(cls, id:str) -> object:
        """Get specific user"""
        try:
            user = cls.objects.get(id=id)
        except Exception as excp:
            user = None
        return user
    

    @classmethod
    def get_user_by_username(cls, username:str) -> object:
        """Get user by username"""
        try:
            user = cls.objects.get(username=username)
        except Exception as excp:
            user = None
        return user


    @classmethod
    def get_selected_users(cls, user_ids:str) -> object:
        """Get all users listed in the user_ids list"""
        try:
            user_ids = user_ids if isinstance(user_ids, list) else [user_ids]
            users = cls.objects.filter(pk__in=user_ids)
        except Exception as excp:
            users = None
        return users
    
    @classmethod
    def delete_user(cls, id:str) -> bool:
        """Delete user by ID"""
        try:
            user = cls.objects.filter(id=id)
            user.delete()
            is_success = True
        except Exception as excp:
            is_success = False
        return is_success