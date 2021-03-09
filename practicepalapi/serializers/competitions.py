from rest_framework import serializers
from practicepalapi.models import Competitions

class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competitions
        fields = ('id', 'created_by', 'section')
