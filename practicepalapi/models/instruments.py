from django.db import models

class Instruments(models.Model):
  label = models.CharField(max_length=250, unique=True)
