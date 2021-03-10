import json
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError, HttpResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action, parser_classes
from rest_framework.authtoken.models import Token
from practicepalapi.models import Instruments
from django.contrib.auth.models import User
from practicepalapi.serializers import InstrumentSerializer
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

class InstrumentsViewSet(ModelViewSet):

  def create(self, request):
    new_instrument = Instruments.objects.create(
        label=request.data['label']
    )

    new_instrument.save()

    serializer = InstrumentSerializer(new_instrument, context={'request': request})
    return Response(serializer.data, status=status.HTTP_201_CREATED)

  def list(self, request):
    instruments = Instruments.objects.all()
    serializer = InstrumentSerializer(
      instruments, many=True, context={'request': request}
    )
    return Response(serializer.data)

  def retrieve(self, request, pk=None):
    try:
      instrument = Instruments.objects.get(pk=pk)
      serializer = InstrumentSerializer(instrument, context={'request': request})
      return Response(serializer.data)
    except Instruments.DoesNotExist:
            return Response({"msg": "Instrument not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as ex:
            return HttpResponseServerError(ex)

  def update(self, request, pk=None):
    try:
      instrument = Instruments.objects.get(pk=pk)
      instrument.label = request.data['label'] or instrument.label

      instrument.save()
      serializer = InstrumentSerializer(instrument)
      return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

    except instrument.DoesNotExist:
        return Response({"msg": "AppUser not found"}, status=status.HTTP_404_NOT_FOUND)

    except Exception as ex:
        return HttpResponseServerError(ex)

  def destroy(self, request, pk=None):
      try:
        instrument = Instruments.objects.get(pk=pk)
        instrument.delete()

        return Response({"msg": "instrument has been succesfully deleted"}, status=status.HTTP_200_OK)

      except instrument.DoesNotExist as ex:
        return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

      except Exception as ex:
        return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
