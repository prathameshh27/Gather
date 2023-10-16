from rest_framework import serializers
from apps.home.models.user import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """Model: CustomUser"""

    class Meta:
        """Metadata for the User Serializer"""
        model = CustomUser
        fields = ('id', 'username', 'first_name', 'last_name', 'display_name', 'email', 'date_joined')

    # Fields
    username = serializers.CharField(min_length=3, max_length=64, trim_whitespace=True)
    display_name = serializers.CharField(source="get_full_name", read_only=True, trim_whitespace=True)
    date_joined = serializers.DateTimeField(read_only=True)


    def update(self, instance, validated_data):
        validated_data.pop('username', None)
        validated_data.pop('date_joined', None)
        instance = super(UserSerializer,self).update(instance, validated_data)
        return instance