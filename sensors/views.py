import sys
import json
import math

from netaddr import EUI, mac_eui48
from macaddress import format_mac

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core import serializers

from .models import Sensor

def index(request):
    sensors = list(Sensor.objects.all().values())

    # Displaying a grid of sensors requires calculating the number of 
    # columns and to make a decent rectangle/square
    numSensors = len(sensors)
    sqrtSensors = math.sqrt(numSensors)
    numCols = math.ceil(sqrtSensors)
    if numSensors == 0:
        colSize =  0
        colWidth = 0
    else:
        colSize = numCols * (numCols / numSensors)
        colWidth = 100 / colSize

    template = loader.get_template("index.html")
    context = {
        "sensors": sensors,
        "colWidth": colWidth,
        "colSize": colSize,
    }
    return HttpResponse(template.render(context, request))

def sensors(request):
    sensors = list(Sensor.objects.all().values())
    return JsonResponse({"status": "ok", "sensors": sensors}, status=200)

@csrf_exempt
def heartbeat(request): 
    # This endpoint only accepts posts containing JSON
    if request.method != "POST":
        body = {"status": "error", "message": "Unsupported HTTP method. POST expected."}
        return JsonResponse(body, status=405)
    if request.content_type != "application/json":
        body = {"status": "error", "message": "Unsupported content type. JSON expected."}
        return JsonResponse(body, status=405)

    # Process the JSON body and report invalid JSON
    try:
        data = json.loads(request.body)
    except ValueError:
        body = {"status": "error", "message": "Body is missing or invalid JSON."}
        return JsonResponse(body, status=400) 

    # Validate JSON payload
    if data["mac_address"] == None:
        body = {"status": "error", "message": "Body must contain mac_address field"}
        return JsonResponse(body, status=400) 

    # Parse and format the MAC address
    try:
        macAddress = EUI(data["mac_address"])
        macAddress = format_mac(macAddress, mac_eui48)
    except:
        body = {"status": "error", "message": "Invalid data. Check that mac_address is valid."}
        return JsonResponse(body, status=400)

    # Upsert sensor with new heartbeat and handle invalid data or infrastructure issues
    try:
        updatedValues = {"last_heartbeat": timezone.now()}
        sensor, created = Sensor.objects.update_or_create(
            mac_address=macAddress,
            defaults=updatedValues)
    except:
        # TODO this should be logged and reported to metrics
        print(sys.exc_info()[0])
        body = {"status": "error", "message": "Sorry, something went wrong. Try again latter."}
        return JsonResponse(body, status=500)

    return JsonResponse({"status": "ok"}, status=200)
  