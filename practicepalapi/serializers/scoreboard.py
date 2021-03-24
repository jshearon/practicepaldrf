from rest_framework import serializers
from rest_framework.fields import CharField
from practicepalapi.models import AppUsers, Sections

class ScoreboardSerializer(serializers.Serializer):
    section = serializers.DictField
    users = serializers.ListField
