import json
from django.core.exceptions import ValidationError
from django.db import IntegrityError
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
    try:
      section = Sections.objects.get(pk=request.data['section'])
      created_by = AppUsers.objects.get(pk=request.user.id)
      new_competition = Competitions.objects.create(
          section = section,
          created_by = created_by
      )

      new_competition.save()

      serializer = CompetitionSerializer(new_competition, context={'request': request})
      return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Sections.DoesNotExist:
            return Response({"msg": "Section does not exist"}, status=status.HTTP_404_NOT_FOUND)
    except IntegrityError:
            return Response({"msg": "User may only subscribe to section once"}, status=status.HTTP_404_NOT_FOUND)
    except ValidationError as ex:
      return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

  def list(self, request):
    competitions = Competitions.objects.all()
    serializer = CompetitionSerializer(
      competitions, many=True, context={'request': request}
    )
    return Response(serializer.data)

  def retrieve(self, request, pk=None):
    try:
      competition = Competitions.objects.get(pk=pk)
      serializer = CompetitionSerializer(competition, context={'request': request})
      return Response(serializer.data)
    except Competitions.DoesNotExist:
            return Response({"msg": "Competition does not exist"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as ex:
            return HttpResponseServerError(ex)

  def destroy(self, request, pk=None):
      try:
        competition = Competitions.objects.get(pk=pk)
        competition.delete()

        return Response({"msg": "Competition has been succesfully deleted"}, status=status.HTTP_200_OK)

      except Competitions.DoesNotExist as ex:
        return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

      except Exception as ex:
        return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
