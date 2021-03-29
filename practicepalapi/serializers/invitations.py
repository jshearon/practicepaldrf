from rest_framework import serializers
from practicepalapi.models import Invitations

class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitations
        fields = ('id', 'inviter', 'invitee', 'section')
        depth = 2
