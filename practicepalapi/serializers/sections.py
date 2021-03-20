from rest_framework import serializers
from practicepalapi.models.sections import Sections, AppUsers, Attempts
from django.db.models import Max
import math
from rest_framework.fields import CurrentUserDefault
class SectionSerializer(serializers.ModelSerializer):

    percent_complete = serializers.SerializerMethodField() 
    complete = serializers.SerializerMethodField() 
    current_tempo = serializers.SerializerMethodField()
    class Meta:
        model = Sections
        fields = ('id', 'song', 'label', 'initial_bpm', 'target_bpm', 'pdf_page_nums', 'beats', 'division', 'tries', 'section_users', 'percent_complete', 'complete', 'current_tempo')
        depth = 2

    def get_percent_complete(self, obj):
        user =  self.context['request'].user
        appuser = AppUsers.objects.get(user__id=user.id)
        attempts = Attempts.objects.filter(
            section__id=obj.id,
            success=True,
            user=appuser.id 
            )
        if attempts:
            latest_attempt = attempts.aggregate(Max('bpm'))
            percent = math.floor(round(100 * (latest_attempt['bpm__max'] / obj.target_bpm), 0))
            return percent
        else:
            return 0
    
    def get_complete(self, obj):
        user =  self.context['request'].user
        appuser = AppUsers.objects.get(user__id=user.id)
        attempts = Attempts.objects.filter(
            section__id=obj.id,
            success=True,
            user=appuser.id 
            )
        latest_attempt = attempts.aggregate(Max('bpm'))
        latest_bpm_count = Attempts.objects.filter(
            section__id=obj.id,
            success=True, 
            bpm=latest_attempt['bpm__max'],
            user=appuser.id 
            ).count()
        if latest_attempt['bpm__max'] == obj.target_bpm and latest_bpm_count == obj.tries:
            return True
        else:
            return False

    def get_current_tempo(self, obj):
        user =  self.context['request'].user
        appuser = AppUsers.objects.get(user__id=user.id)
        attempts = Attempts.objects.filter(
            section__id=obj.id,
            success=True,
            user=appuser.id 
            )
        latest_attempt = attempts.aggregate(Max('bpm'))
        latest_bpm_count = Attempts.objects.filter(
            section__id=obj.id,
            success=True, 
            bpm=latest_attempt['bpm__max'],
            user=appuser.id 
            ).count()
        if latest_bpm_count == obj.tries:
            return latest_attempt['bpm__max'] + 1
        elif latest_attempt['bpm__max'] is None:
            return obj.initial_bpm
        else:
            return latest_attempt['bpm__max']
