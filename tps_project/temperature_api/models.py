from django.db import models

# Create your models here.

class TemperatureMeasurementModel(models.Model):
    
    # Fields
    time = models.DateTimeField()  # Represents the timestamp for the data point
    value = models.FloatField()    # Represents the temperature value for the data point

    class Meta:
        db_table = "temperature"   # Set the database table name to match the InfluxDB measurement
        #managed = False


    @classmethod
    def fetch_data(cls):
        print("FEtCH DATA...")
        influx_client = get_influxdb_client()
        # Implement the query to fetch data from the remote InfluxDB using the influx_client.
        # Process the fetched data and return it.
        pass