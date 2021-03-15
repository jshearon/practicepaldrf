import json
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError, HttpResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action, parser_classes
from rest_framework.authtoken.models import Token
from practicepalapi.models import AppUsers
from django.contrib.auth.models import User
from practicepalapi.serializers import AppUserSerializer
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from django.views.decorators.csrf import csrf_exempt

class AppUsersViewSet(ModelViewSet):

  def list(self, request):
    users = AppUsers.objects.all()
    serializer = AppUserSerializer(
      users, many=True, context={'request': request}
    )
    return Response(serializer.data)

  def retrieve(self, request, pk=None):
    try:
      appuser = AppUsers.objects.get(pk=pk)
      serializer = AppUserSerializer(appuser, context={'request': request})
      return Response(serializer.data)
    except AppUsers.DoesNotExist:
            return Response({"msg": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as ex:
            return HttpResponseServerError(ex)

  def update(self, request, pk=None):
    try:
      appuser = AppUsers.objects.get(pk=pk)
      user = User.objects.get(pk=appuser.user.id)
    
      appuser.profile_image = request.data['profile_image'] or appuser.profile_image
      user.username = request.data['username'] or user.username
      user.first_name = request.data['first_name'] or user.first_name
      user.last_name = request.data['last_name'] or user.last_name
      user.email = request.data['email'] or user.email
      user.password = request.data['password'] or user.password
      
      appuser.user = user

      user.save()
      appuser.save()

      return Response({"msg": "user updated"}, status=status.HTTP_204_NO_CONTENT)
    except appuser.DoesNotExist:
        return Response({"msg": "AppUser not found"}, status=status.HTTP_404_NOT_FOUND)
    except user.DoesNotExist:
        return Response({"msg": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as ex:
        return HttpResponseServerError(ex)

  def destroy(self, request, pk=None):
      try:
        appuser = AppUsers.objects.get(pk=pk)
        username = appuser.user.username
        appuser.delete()

        return Response({"msg": "user " + username + " has been succesfully deleted"}, status=status.HTTP_200_OK)

      except AppUsers.DoesNotExist as ex:
        return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

      except Exception as ex:
        return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

  @action(methods=['get'], detail=False)   
  def profile(self, request, pk=None):
    try:
      appuser = AppUsers.objects.get(user=request.user.id)
      serializer = AppUserSerializer(appuser, context={'request': request})
      return Response(serializer.data)
    except AppUsers.DoesNotExist:
            return Response({"msg": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as ex:
            return HttpResponseServerError(ex)
