from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE

class Songs(models.Model):
  title = models.CharField(max_length=250)
  composer = models.CharField(max_length=250)
  pdf = models.FileField(upload_to='pdfs/', null=True, blank=True )
  instrument = models.ForeignKey(
    "Instruments", 
    on_delete=CASCADE, 
    related_name="instruments",
    related_query_name="instrument"
    )
  user = models.ForeignKey(
    "AppUsers",
    on_delete=CASCADE,
    related_name="appusers",
    related_query_name="appuser"
  )
