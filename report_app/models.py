from django.db import models

# Create your models here.
from django.db import models
from timezone_field import TimeZoneField

class TimeSeries(models.Model):
    timestamp = models.DateTimeField(unique=True)
    value = models.FloatField()
    timezone = TimeZoneField(default='UTC')