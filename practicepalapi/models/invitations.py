from django.db import models
from django.db.models.deletion import CASCADE
from .appusers import AppUsers
from .sections import Sections

class Invitations(models.Model):
  inviter = models.ForeignKey(
    "AppUsers",
    on_delete=CASCADE,
    related_name="inviter_appusers",
    related_query_name="inviter_appuser"
  )
  invitee = models.ForeignKey(
    "AppUsers",
    on_delete=CASCADE,
    related_name="invitee_appusers",
    related_query_name="invitee_appuser"
  )
  section = models.ForeignKey(
    "Sections",
    on_delete=CASCADE,
    related_name="invite_sections",
    related_query_name="invite_section"
  )
