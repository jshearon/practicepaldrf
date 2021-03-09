from rest_framework import serializers
from practicepalapi.models import AppUsers

class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUsers
        fields = ('id', 'user', 'profile_image')
