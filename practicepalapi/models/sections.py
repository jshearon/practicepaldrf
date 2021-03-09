from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE

class Sections(models.Model):
  song = models.ForeignKey("Songs", on_delete=models.CASCADE)
  label = models.CharField(max_length=50)
  initial_bpm = models.IntegerField()
  target_bpm = models.IntegerField()
  is_complete = models.BooleanField(default=False)
  pdf_page_nums = models.JSONField()
  beats = models.IntegerField(default=4)
  division = models.IntegerField(default=4)
  section_users = models.ManyToManyField(
    "AppUsers",
    related_name="section_users", 
    related_query_name="sections_user"
  )
