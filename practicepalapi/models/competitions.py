from django.db import models
from django.db.models.deletion import CASCADE

class Competitions(models.Model):
  created_by = models.ForeignKey(
    "AppUsers",
    on_delete=CASCADE,
    related_name="competition_creators",
    related_query_name="competition_creator"
  )
  section = models.ForeignKey(
    "Sections",
    on_delete=CASCADE,
    related_name="competition_sections",
    related_query_name="competition_section"
  )
