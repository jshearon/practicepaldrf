from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE

class AppUsers(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=CASCADE)
  profile_image = models.ImageField(upload_to="userimages/", default = 'userimages/None/no-img.jpg')
