from rest_framework import serializers
from practicepalapi.models import Songs

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Songs
        fields = ('id', 'title', 'composer', 'pdf', 'instrument', 'user')
