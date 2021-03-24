import json
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError, HttpResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action, parser_classes
from rest_framework.authtoken.models import Token
from practicepalapi.models import Sections, Songs, AppUsers, Attempts
from practicepalapi.serializers import SectionSerializer, ScoreboardSerializer
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from django.db.models import Max
from django.db.models.functions import Length
import math

class SectionsViewSet(ModelViewSet):

  def create(self, request):
    appuser = AppUsers.objects.get(user_id=request.user.id)
    song = Songs.objects.get(pk=request.data['song'])
    new_section = Sections.objects.create(
        song = song,
        label = request.data['label'],
        initial_bpm = request.data['initial_bpm'],
        target_bpm = request.data['target_bpm'],
        is_complete = False,
        pdf_page_nums = request.data['pdf_page_nums'],
        beats = request.data['beats'],
        division = request.data['division'],
        tries = request.data['tries']
    )

    try:
      new_section.save()
      new_section.section_users.set([appuser])
      new_section.save()

      serializer = SectionSerializer(new_section, context={'request': request})
      return Response(serializer.data, status=status.HTTP_201_CREATED)

    except ValidationError as ex:
      return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

  def list(self, request):
    if request.GET.get('user'):
      appuser = AppUsers.objects.get(user_id=request.user.id)
      sections = Sections.objects.filter(section_users=appuser.id)
    else:
      sections = Sections.objects.all()
    serializer = SectionSerializer(
      sections, many=True, context={'request': request}
    )
    return Response(serializer.data)

  def retrieve(self, request, pk=None):
    try:
      section = Sections.objects.get(pk=pk)
      serializer = SectionSerializer(section, context={'request': request})
      return Response(serializer.data)
    except Sections.DoesNotExist:
            return Response({"msg": "Section does not exist"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as ex:
            return HttpResponseServerError(ex)

  def update(self, request, pk=None):
    try:
      song = Songs.objects.get(pk=request.data['song'])
      section = Sections.objects.get(pk=pk)
      section.song = song
      section.label = request.data['label']
      section.initial_bpm = request.data['initial_bpm']
      section.target_bpm = request.data['target_bpm']
      section.is_complete = False
      section.pdf_page_nums = request.data['pdf_page_nums']
      section.beats = request.data['beats']
      section.division = request.data['division']
      section.tries = request.data['tries']
      if request.data.get("section_users"):
        section.section_users.set(request.data['section_users'])

      section.save()

      serializer = SectionSerializer(section, context={"request":request})

      return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

    except Sections.DoesNotExist:
        return Response({"msg": "Song does not exist"}, status=status.HTTP_404_NOT_FOUND)

    except Exception as ex:
        return HttpResponseServerError(ex)

  def destroy(self, request, pk=None):
      try:
        section = Sections.objects.get(pk=pk)
        section.delete()

        return Response({"msg": "Song has been succesfully deleted"}, status=status.HTTP_200_OK)

      except Songs.DoesNotExist as ex:
        return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

      except Exception as ex:
        return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
  @action(methods=['GET'], detail=True)
  def scoreboard(self, request, pk=None):
    try:
      grouped_obj = []
      appuser = AppUsers.objects.get(user_id=request.user.id)
      sections = Sections.objects.filter(section_users = appuser)
      for section in sections:
        section_scoreboard = {}
        # section_scoreboard.title = section.song.title
        section_scoreboard.label = section.label
        section_scoreboard.users = []
        users = section.section_users.all()
        for user in users:
          add_user = {}
          add_user.profile_image = user.profile_image
          add_user.first_name = user.user.first_name
          add_user.last_name = user.user.last_name
          attempts = Attempts.objects.filter(
              section__id=section.id,
              success=True,
              user=user.id 
              )
          latest_attempt = attempts.aggregate(Max('bpm'))
          add_user.bmp = latest_attempt
        section_scoreboard.users = add_user  
        json_data = json.dumps(section_scoreboard)
      return Response( json_data, status=status.HTTP_204_NO_CONTENT)
    except Exception as ex:
      return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
