import json
import re
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError, HttpResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action, parser_classes
from rest_framework.authtoken.models import Token
from practicepalapi.models import Sections, Songs, AppUsers, Attempts
from practicepalapi.serializers import SectionSerializer
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from django.db.models import Max
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
      sections = Sections.objects.filter(section_users__id__contains=appuser.id)
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
      print(section, request.data)
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
    def scoreboard(self, request:
      try:
        appuser = AppUsers.objects.get(user_id=request.user.id)
        sections = Sections.objects.filter(section_users__id__contains=appuser.id))
      except Exception as ex:
        return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
