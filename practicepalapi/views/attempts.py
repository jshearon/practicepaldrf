import json
import datetime
from django.core.exceptions import ValidationError
from django.db.models.fields import DateTimeField
from django.http import HttpResponseServerError, HttpResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action, parser_classes
from rest_framework.authtoken.models import Token
from practicepalapi.models import Attempts, Sections, AppUsers
from practicepalapi.serializers import AttemptSerializer
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

class AttemptsViewSet(ModelViewSet):

  def create(self, request):
    appuser = AppUsers.objects.get(user=request.user)
    section = Sections.objects.get(pk=request.data['section'])
    new_attempt = Attempts.objects.create(
        section = section,
        bpm = request.data['bpm'],
        success = request.data['success'],
        attempted_on = datetime.datetime.now(),
        user = appuser
    )

    try:
      new_attempt.save()

      serializer = AttemptSerializer(new_attempt, context={'request': request})
      return Response(serializer.data, status=status.HTTP_201_CREATED)

    except ValidationError as ex:
      return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

  def list(self, request):
    attempts = Attempts.objects.all()
    serializer = AttemptSerializer(
      attempts, many=True, context={'request': request}
    )
    return Response(serializer.data)

  def retrieve(self, request, pk=None):
    try:
      attempt = Attempts.objects.get(pk=pk)
      serializer = AttemptSerializer(attempt, context={'request': request})
      return Response(serializer.data)
    except Attempts.DoesNotExist:
            return Response({"msg": "Attempt does not exist"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as ex:
            return HttpResponseServerError(ex)


  def destroy(self, request, pk=None):
      try:
        attempt = Attempts.objects.get(pk=pk)
        attempt.delete()

        return Response({"msg": "Attempt has been succesfully deleted"}, status=status.HTTP_200_OK)

      except Attempts.DoesNotExist as ex:
        return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

      except Exception as ex:
        return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
