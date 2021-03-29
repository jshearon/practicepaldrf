import json
from practicepalapi.models import sections
from practicepalapi.models.appusers import AppUsers
from practicepalapi.models.sections import Sections
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError, HttpResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action, parser_classes
from rest_framework.authtoken.models import Token
from practicepalapi.models import Invitations, invitations
from django.contrib.auth.models import User
from practicepalapi.serializers import InvitationSerializer
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

class InvitationsViewSet(ModelViewSet):

  def create(self, request):
    inviter = AppUsers.objects.get(user_id=request.user.id)
    invitee = AppUsers.objects.get(user_id=request.data['invitee'])
    section = Sections.objects.get(pk=request.data['section'])

    new_invitation = Invitations.objects.create(
        inviter=inviter,
        invitee=invitee,
        section=section
    )

    new_invitation.save()

    serializer = InvitationSerializer(new_invitation, context={'request': request})
    return Response(serializer.data, status=status.HTTP_201_CREATED)

  def list(self, request):
    invitations = Invitations.objects.all()
    serializer = InvitationSerializer(
      invitations, many=True, context={'request': request}
    )
    return Response(serializer.data)

  def retrieve(self, request, pk=None):
    try:
      invitation = Invitations.objects.get(pk=pk)
      serializer = InvitationSerializer(invitation, context={'request': request})
      return Response(serializer.data)
    except Invitations.DoesNotExist:
            return Response({"msg": "Invitation not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as ex:
            return HttpResponseServerError(ex)

  def destroy(self, request, pk=None):
      try:
        invitation = Invitations.objects.get(pk=pk)
        invitation.delete()

        return Response({"msg": "invitation has been succesfully deleted"}, status=status.HTTP_200_OK)

      except invitation.DoesNotExist as ex:
        return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

      except Exception as ex:
        return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

  @action(methods=['POST'], detail=True)
  def accept(self, request, pk=None):
    try:
      invitation = Invitations.objects.get(pk=pk)
      section = Sections.objects.get(pk=invitation.section.id)
      section.section_users.add(invitation.invitee)
      section.save()
      invitation.delete()

      return Response({"msg": "invitation has been accepted"}, status=status.HTTP_200_OK)
    
    except Invitations.DoesNotExist as ex:
        return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    except Sections.DoesNotExist as ex:
        return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    except Exception as ex:
        return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
