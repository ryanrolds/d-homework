from django.db import models
from macaddress.fields import MACAddressField

class Sensor(models.Model):
    mac_address = models.CharField(primary_key=True, max_length=17)
    last_heartbeat = models.DateTimeField()
