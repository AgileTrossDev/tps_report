from django.db import models

# Create your models here.


class TemperatureMeasurementModel(models.Model):

    # Fields
    time = models.DateTimeField()  # Represents the timestamp for the data point
    value = models.FloatField()    # Represents the temperature value for the data point

    class Meta:
        # Set the database table name to match the InfluxDB measurement
        db_table = "temperature"
        # managed = False
