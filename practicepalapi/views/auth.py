import json
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError, HttpResponse, HttpResponseNotAllowed
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
from django.contrib.auth import authenticate

@csrf_exempt
def register(request):
  new_user = User.objects.create_user(
      username=request.POST['email'],
      email=request.POST['email'],
      password=request.POST['password'],
      first_name=request.POST['firstName'],
      last_name=request.POST['lastName']
  )

  appuser = AppUsers.objects.create(
    user=new_user,
    profile_image=request.FILES.get('profileImage', None)
  )

  serializer = AppUserSerializer(data=appuser, context={'request': request})
  if serializer.is_valid():
    serializer.save()

  token = Token.objects.create(user=new_user)
  data = json.dumps({"token": token.key, "id": new_user.id})
  return HttpResponse(data, content_type='application/json', status=status.HTTP_201_CREATED)

@csrf_exempt
def login(request):

    body = request.body.decode('utf-8')
    req_body = json.loads(body)

    if request.method == 'POST':

        name = req_body['username']
        pw = req_body['password']
        authenticated_user = authenticate(username=name, password=pw)

        if authenticated_user is not None:
            token = Token.objects.get(user=authenticated_user)
            data = json.dumps({"valid": True, "token": token.key, "id": authenticated_user.id})
            return HttpResponse(data, content_type='application/json')

        else:
            data = json.dumps({"valid": False})
            return HttpResponse(data, content_type='application/json')

    return HttpResponseNotAllowed(permitted_methods=['POST'])
