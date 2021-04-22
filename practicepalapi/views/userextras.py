import json
from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework.decorators import action, parser_classes
from rest_framework.authtoken.models import Token
from practicepalapi.models import AppUsers, Sections, Attempts
from rest_framework import viewsets
from django.db.models import Max

class ScoreboardViewSet(viewsets.ViewSet):
  def list(self, request):
    data = []

    appuser = AppUsers.objects.get(user__id=request.user.id)
    sections = Sections.objects.filter(section_users=appuser)

    for section in sections:
      new_section = dict(
        id = section.id,
        song = section.song.title,
        label = section.label,
        competitors = [],
      )
      for section_user in section.section_users.all():
        competitor = dict(
          profile_image = request.build_absolute_uri(section_user.profile_image.url),
          first_name = section_user.user.first_name,
          last_name = section_user.user.last_name,
        )
        attempts = Attempts.objects.filter(
            section__id=section.id,
            success=True,
            user=section_user.id 
            )
        latest_attempt = attempts.aggregate(Max('bpm'))
        competitor['bpm'] = section.initial_bpm if latest_attempt['bpm__max'] is None else latest_attempt['bpm__max']
        new_section['competitors'].append(competitor)
        sorted_section = sorted(new_section['competitors'], key = lambda i: i['bpm'], reverse=True)
        new_section['competitors'] = sorted_section
      if len(new_section['competitors']) > 1:
        data.append(new_section)


    #loop through users and get highest bpm

    return HttpResponse(json.dumps(data), content_type='application/json')


def competitors(request):
  data = []

  if request.GET.get('section') and request.GET.get('q'):
    section = Sections.objects.get(pk=request.GET.get('section'))
    players = AppUsers.objects.filter(user__username__contains=request.GET.get('q'))

    for player in players:
      if player not in section.section_users.all():
        add_player = dict(
          id = player.id,
          profile_image = request.build_absolute_uri(player.profile_image.url),
          first_name = player.user.first_name,
          last_name = player.user.last_name,
        )
        data.append(add_player)

    return HttpResponse(json.dumps(data), content_type='application/json')
  else:
    return HttpResponse(json.dumps([]), content_type='application/json')
