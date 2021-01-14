from django.db import models
from macaddress.fields import MACAddressField

class Sensor(models.Model):
    mac_address = MACAddressField(primary_key=True, integer=False)
    last_heartbeat = models.DateTimeField()
