from rest_framework import serializers
from practicepalapi.models.sections import Sections
class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sections
        fields = ('id', 'song', 'label', 'initial_bpm', 'target_bpm', 'pdf_page_nums', 'beats', 'division', 'tries', 'section_users', 'percent_complete', 'complete')
        depth = 2
