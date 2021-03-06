from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE

class Attempts(models.Model):
  section = models.ForeignKey(
    "Sections",
    on_delete=CASCADE,
    related_name="section_attempts",
    related_query_name="section_attempt"
  )
  bpm = models.IntegerField()
  success = models.BooleanField()
  attempted_on = models.DateTimeField(auto_now_add=True)
  user = models.ForeignKey(
    "AppUsers",
    on_delete=CASCADE,
    related_name="user_attempts",
    related_query_name="user_attempt"
  )
