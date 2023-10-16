from datetime import timedelta
from django.utils import timezone

from rest_framework import serializers

from apps.home.models.meeting import Meeting
from apps.home.models.user import CustomUser


class MeetingSerializer(serializers.ModelSerializer):
    """Model: Meeting"""

    class Meta:
        """Metadata for the User Serializer"""
        model = Meeting
        fields = ('id', 'title', 'description', 'created_by', 'attendees', 'starts_at', 'ends_at')

    MIN_INTERVAL = 10       # Min Meeting duration in minutes
    ATOMIC_INTERVAL = 5     # Entered time must me a multiple of ATOMIC_INTERVAL

    # Fields:
    title = serializers.CharField(min_length=3, max_length=128, trim_whitespace=True)
    created_by = serializers.CharField()
    attendees = serializers.SlugRelatedField(many=True, slug_field='username', queryset=CustomUser.objects.all(), required=False)

    def check_users_availability(self, attendees:list, starts_at:str, ends_at:str) -> tuple:
        """Takes attendees and timeframe to check availability of each user"""
        available_users, unavailable_users = [],[]

        # seperates available and unavailable users
        for attendee in attendees:
            user = CustomUser.get_user_by_username(attendee)
            if user:
                attendee = str(attendee)
                # calls the user method to check availability
                is_available = user.check_schedule_conflict(starts_at, ends_at)

                if is_available:
                    available_users.append(attendee)
                else:
                    unavailable_users.append(attendee)

            else:
                unavailable_users.append(attendee)

        return available_users, unavailable_users


    def validate(self, attrs):
        """Validate meeting details before saving it into the Database"""

        starts_at = attrs.get('starts_at', None)
        ends_at = attrs.get('ends_at', None)

        datetime_now = timezone.now()

        if starts_at and starts_at <= datetime_now:
            raise serializers.ValidationError("starts_at must be in the future")
        
        if starts_at and (starts_at.minute % self.ATOMIC_INTERVAL != 0):
            raise serializers.ValidationError(f"starts_at:minutes must be multiple of {self.ATOMIC_INTERVAL}")

        if ends_at and ends_at <= datetime_now:
            raise serializers.ValidationError("ends_at must be in the future")
        
        if ends_at and (ends_at.minute % self.ATOMIC_INTERVAL != 0):
            raise serializers.ValidationError(f"ends_at:minutes must be multiple of {self.ATOMIC_INTERVAL}")

        if starts_at and ends_at and (starts_at + timedelta(minutes=self.MIN_INTERVAL)) > ends_at:
            raise serializers.ValidationError(f"ends_at must be greater than starts_at and the min interval must be {self.MIN_INTERVAL} mins.")

        return attrs
    

    def create(self, validated_data):
        # This function will allow the meeting owner to create a meeting
        # even if the owner has a conflicting schedule.
        # It is assumed that the user is aware of their conflicting schedule
        # and they still wish to schedule this meeting.

        created_by = validated_data.pop('created_by', None)
        attendees  = validated_data.pop('attendees', None)
        starts_at  = validated_data.get('starts_at', None)
        ends_at    = validated_data.get('ends_at', None)

        meeting_admin = CustomUser.get_user(id=created_by)

        if (not starts_at) or (not ends_at):
            raise Exception("field named starts_at, ends_at are mandatory.")

        # By default assigns the logged user as the owner of the meeting 
        if meeting_admin:
            validated_data["created_by"] = meeting_admin
        else:
            raise Exception("Invalid entry in created_by field. User not found.")

        available_users, unavailable_users = self.check_users_availability(attendees, starts_at, ends_at)

        if len(available_users) == 0:
            raise Exception("The supplied users are unavailable for this meeting. Please choose a diffrent timeslot")

        attendees = available_users

        meeting = Meeting.objects.create(**validated_data)

        meeting.add_attendees(attendees)
        meeting.unavailable_users = unavailable_users

        return meeting


    def update(self, instance, validated_data):
        """supports Partial update"""
        unavailable_users = []
        
        created_by = validated_data.pop('created_by', None)
        attendees = validated_data.get('attendees', None)
        starts_at  = str(instance.starts_at)
        ends_at    = str(instance.ends_at)

        user = CustomUser.get_user_by_username(created_by)
        
        if isinstance(attendees, list):

            available_users, unavailable_users = self.check_users_availability(attendees, starts_at, ends_at)
            attendees = available_users
            attendees.append(user)

        instance = super(MeetingSerializer,self).update(instance, validated_data)

        validated_data['unavailable_users'] = unavailable_users
        return instance
    