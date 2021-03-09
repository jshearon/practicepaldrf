from rest_framework import serializers
from practicepalapi.models import AppUsers

class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUsers
        fields = ('id', 'song', 'label', 'initial_bpm', 'target_bpm', 'is_complete', 'pdf_page_nums', 'beats', 'division', 'tries', 'section_users')
