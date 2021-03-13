from rest_framework import serializers
from django.contrib.auth.models import User
from practicepalapi.models import AppUsers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password')
class AppUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = AppUsers
        fields = ('id', 'user', 'profile_image')
        depth=1
