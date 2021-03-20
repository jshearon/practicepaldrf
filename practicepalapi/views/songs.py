import json
from practicepalapi.models.instruments import Instruments
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError, HttpResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action, parser_classes
from rest_framework.authtoken.models import Token
from practicepalapi.models import Songs, AppUsers
from practicepalapi.serializers import SongSerializer
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

class SongsViewSet(ModelViewSet):

  def create(self, request):
    instrument = Instruments.objects.get(pk=request.data['instrument'])
    appuser = AppUsers.objects.get(user=request.user)
    new_song = Songs.objects.create(
        title = request.data['title'],
        composer = request.data['composer'],
        pdf = request.data['pdf'],
        instrument = instrument,
        user = appuser
    )

    new_song.save()

    serializer = SongSerializer(new_song, context={'request': request})
    return Response(serializer.data, status=status.HTTP_201_CREATED)

  def list(self, request):
    if request.GET.get('user'):
      appuser = AppUsers.objects.get(user_id=request.user.id)
      songs = Songs.objects.filter(user__id=appuser.id)
    else:
      songs = Songs.objects.all()
    serializer = SongSerializer(
      songs, many=True, context={'request': request}
    )
    return Response(serializer.data)

  def retrieve(self, request, pk=None):
    try:
      song = Songs.objects.get(pk=pk)
      serializer = SongSerializer(song, context={'request': request})
      return Response(serializer.data)
    except Songs.DoesNotExist:
            return Response({"msg": "Song does not exist"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as ex:
            return HttpResponseServerError(ex)

  def update(self, request, pk=None):
    try:
      song = Songs.objects.get(pk=pk)
      instrument = Instruments.objects.get(pk=request.data['instrument'])
      song.title = request.data['title']
      song.composer = request.data['composer']
      song.instrument = instrument
      song.pdf = request.data['pdf']

      song.save()

      serializer = SongSerializer(song)

      return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

    except Songs.DoesNotExist:
        return Response({"msg": "Song does not exist"}, status=status.HTTP_404_NOT_FOUND)

    except Exception as ex:
        return HttpResponseServerError(ex)

  def destroy(self, request, pk=None):
      try:
        song = Songs.objects.get(pk=pk)
        song.delete()

        return Response({"msg": "Song has been succesfully deleted"}, status=status.HTTP_200_OK)

      except Songs.DoesNotExist as ex:
        return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

      except Exception as ex:
        return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
