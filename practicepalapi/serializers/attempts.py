from practicepalapi.models.attempts import Attempts
from rest_framework import serializers
from practicepalapi.models import Attempts

class AttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attempts
        fields = ('id', 'section', 'bpm', 'success', 'attempted_on', 'user')
