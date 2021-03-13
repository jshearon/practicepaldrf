import json
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError, HttpResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action, parser_classes
from rest_framework.authtoken.models import Token
from practicepalapi.models import Competitions, Sections, Songs, AppUsers
from practicepalapi.serializers import CompetitionSerializer
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

class CompetitionsViewSet(ModelViewSet):

  def create(self, request):
    section = Sections.objects.get(pk=request.data['section'])
    created_by = AppUsers.objects.get(pk=request.user.id)
    new_competition = Competitions.objects.create(
        section = section,
        created_by = created_by
    )

    try:
      new_competition.save()

      serializer = CompetitionSerializer(new_competition, context={'request': request})
      return Response(serializer.data, status=status.HTTP_201_CREATED)

    except ValidationError as ex:
      return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

  def list(self, request):
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
      section = Sections.objects.get(pk=pk)
      for key, val in request.data.items():
        if key == 'song':
          song = Songs.objects.get(pk=val)
          section.song = song,
        elif key == 'section_users':
          section.section_users.set(val)
        else:
          if hasattr(section, key):
            setattr(section, key, val)

      section.save()

      serializer = SectionSerializer(section)

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
