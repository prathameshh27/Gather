from django.db import models
from apps.lib.utils.functions import custom_id
from .user import CustomUser
from django.utils import timezone
from django.conf import settings


class Meeting(models.Model):

    class Meta:
        ordering = ('-starts_at', '-ends_at')

    MAX_ATTENDEES = 50
    IST_TZ = settings.IST_TZ

    id = models.CharField(primary_key=True, unique=True, editable=False, default=custom_id, max_length=11)
    title = models.CharField(null=False, max_length=128)
    description = models.CharField(null=True, blank=True, max_length=500)
    created_by = models.ForeignKey(to=CustomUser, null=False, related_name="meeting_owner", on_delete=models.DO_NOTHING)
    attendees = models.ManyToManyField(to=CustomUser, blank=True, related_name="meeting_attendee")
    starts_at = models.DateTimeField(null=False, blank=False, default="2000-01-01T00:00:00+05:30")
    ends_at = models.DateTimeField(null=False, blank=False, default="2000-01-01T00:00:00+05:30")

    
    # The save method is overridden to add meeting owner to the attendee list by default 
    def save(self, *args, **kwargs):
        super(Meeting, self).save(*args, **kwargs)
        self.add_attendees([self.created_by])


    def get_id(self) -> str:
        """Get meeting ID"""
        return self.id
    
    def get_obj(self) -> object:
        """Get meeting Object"""
        return self
    

    def add_attendees(self, attendees:list) -> bool:
        """Add attendees from the meeting. 
        Pass the attendee IDs in a list even if there is only one attendee"""
        try:
            attendee_count = self.attendees.count()
            if attendee_count <= self.MAX_ATTENDEES:
                add_list = CustomUser.objects.filter(username__in=attendees)
                self.attendees.add(*add_list)
                return True
            else:
                return False
        except Exception as excp:
            return False
        
    def remove_attendees(self, attendees:list) -> bool:
        """Remove attendees from the meeting. 
        Pass the attendee IDs in a list even if there is only one attendee"""
        try:
            rm_list = self.attendees.filter(username__in=attendees)
            self.attendees.remove(*rm_list)
            self.save()
            return True
        except Exception as excp:
            return False   


    @classmethod
    def list_meetings(cls, *args, **kwargs) -> object:
        """List all meetings"""
        return cls.objects.filter(*args, **kwargs)


    @classmethod
    def list_upcoming_meetings(cls, queryset = {}) -> object:
        """List all upcoming meetings"""
        now = timezone.now().astimezone(cls.IST_TZ)
        return cls.objects.filter(starts_at__gte = str(now))
    
    @classmethod
    def get_meeting(cls, id:str) -> object:
        """Get meeting by id"""
        try:
            meeting = cls.objects.get(id=id)
        except Exception as excp:
            meeting = None
        return meeting
    
    @classmethod
    def delete_meeting(cls, id:str) -> bool:
        """delete meeting by id"""
        try:
            meeting = cls.objects.filter(id=id)
            meeting.delete()
            is_success = True
        except Exception as excp:
            is_success = False
        return is_success
    