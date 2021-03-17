from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE
from .attempts import Attempts
from django.db.models import Max
import math

class Sections(models.Model):
  song = models.ForeignKey("Songs", on_delete=models.CASCADE)
  label = models.CharField(max_length=50)
  initial_bpm = models.IntegerField()
  target_bpm = models.IntegerField()
  is_complete = models.BooleanField(default=False)
  pdf_page_nums = models.JSONField()
  beats = models.IntegerField(default=4)
  division = models.IntegerField(default=4)
  tries = models.IntegerField(default=3)
  section_users = models.ManyToManyField(
    "AppUsers",
    related_name="section_users", 
    related_query_name="sections_user"
  )

  @property
  def percent_complete(self):
    attempts = Attempts.objects.filter(
      section__id=self.pk,
      success=True
      )
    if attempts:
      latest_attempt = attempts.aggregate(Max('bpm'))
      percent = math.floor(round(100 * (latest_attempt['bpm__max'] / self.target_bpm), 0))
      return percent
    else:
      return 0

  @property
  def complete(self):
    attempts = Attempts.objects.filter(
      section__id=self.pk,
      success=True
      )
    latest_attempt = attempts.aggregate(Max('bpm'))
    latest_bpm_count = Attempts.objects.filter(
      section__id=self.pk,
      success=True, 
      bpm=latest_attempt['bpm__max']
      )
    if latest_attempt == self.target_bpm and latest_bpm_count == self.tries:
      return True
    else:
      return False
