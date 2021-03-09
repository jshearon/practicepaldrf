from rest_framework import serializers
from practicepalapi.models import Instruments

class InstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instruments
        fields = ('id', 'label')
