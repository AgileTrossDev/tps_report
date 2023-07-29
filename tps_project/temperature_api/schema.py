# GraphQL Schema that works InfluxDB hosting the Temperature Data for the System.
#
# NOTE: Relies on influxdb_connection() to be establish database connection
#       because InfluxDb is not natively supported by Django.
#
import graphene
from datetime import timezone

from tps_project import settings
from graphene_django.types import DjangoObjectType
from .influxdb_connection import get_influxdb_client
from temperature_api.models import TemperatureMeasurementModel


class TemperatureMeasurementType(DjangoObjectType):
    """
    DjangoObjectType for the MeasurementModel.

    NOTE: Since we are using influxdb, we need to set a primary key,
          and override resolve_id in order the query to work
    """
    pk = graphene.String(source='time')

    class Meta:
        model = TemperatureMeasurementModel
        fields = '__all__'  # Include all fields from the Django model

    # Override the 'resolve_id' method to use the custom primary key field as
    # the 'pk' field
    def resolve_id(self, info):
        return self.time

# GraphQL Type that represents the Temperature Statistics


class TemperatureStatistics(graphene.ObjectType):
    min = graphene.Float()      # Min Temp for a Time Range of the Statistics
    max = graphene.Float()      # Max Temp for a Time Range of the Statistics
    valid = graphene.Boolean()  # Flag if Data is Valid

class Query(graphene.ObjectType):
    temperature_measurements = graphene.List(
        TemperatureMeasurementType,
        description="Last 2 Seconds of Temperature measurement.")
    current_temperature = graphene.List(
        TemperatureMeasurementType,
        description="Fetches the most current Temperature value")
    temperatureStatistics = graphene.Field(
        TemperatureStatistics,
        after=graphene.DateTime(),
        before=graphene.DateTime()        
    )

    def resolve_temperature_measurements(self, info):
        """
        Resolver that fetches last 2 seconds of temperature measurements from InfluxDB
        using the influxdb_connection module and return them as Django objects.
        """

        # Get the influx client and perform query
        influx_client = get_influxdb_client()
        query = f'''from(bucket: "{settings.INFLUXDB_BUCKET}")
          |> range(start: -2s)
          |> filter(fn: (r) => r._measurement == "temperature")'''
        result = influx_client.query_api().query(query, org=settings.INFLUXDB_ORG)

        # Buld Return Object
        temperature_measurements = []
        for table in result:
            for record in table.records:
                tmp = TemperatureMeasurementType()
                tmp.time = record['_time']
                tmp.value = record['_value']
                temperature_measurements.append(tmp)

        print("We good?")
        return temperature_measurements

    def resolve_current_temperature(self, info):
        """
        Resolver that fetches the most current Temperature value
        """

        # Get the influx client and perform query
        influx_client = get_influxdb_client()
        query = f'''from(bucket: "{settings.INFLUXDB_BUCKET}")
          |> range(start: -1h)
          |> filter(fn: (r) => r._measurement == "temperature")
          |> last()'''
        result = influx_client.query_api().query(
            query=query, org=settings.INFLUXDB_ORG)

        # Get the first (and only) table from the result
        table = result[0]

        # Get the first (and only) record from the table
        record = table.records[0]

        tmp = TemperatureMeasurementType()
        tmp.time = record['_time']
        tmp.value = record['_value']
        temperature_measurements = []
        temperature_measurements.append(tmp)

        return temperature_measurements

    def resolve_temperatureStatistics(self, info, after, before):
        """
        Queries for the min and max Temperature Measurement

        TODO: Single Query?
        from(bucket: "my-bucket")
        |> range(start: 2023-07-28T15:07:04.942633+00:00, stop: 2023-07-28T15:07:05.942633+00:00)
        |> filter(fn: (r) => r._measurement == "temperature")
        |> min(column: "_value")
        |> yield(name: "min_value")
        |> max(column: "_value")
        |> yield(name: "max_value")
        """
        influx_client = get_influxdb_client()

        q_min = f'''
            from(bucket: "{settings.INFLUXDB_BUCKET}")
              |> range(start: {after.astimezone(timezone.utc).isoformat()},
                stop: {before.astimezone(timezone.utc).isoformat()})
              |> filter(fn: (r) => r._measurement == "temperature")
              |> min(column:"_value")

        '''

        q_max = f'''
            from(bucket: "{settings.INFLUXDB_BUCKET}")
              |> range(start: {after.astimezone(timezone.utc).isoformat()},
                stop: {before.astimezone(timezone.utc).isoformat()})
              |> filter(fn: (r) => r._measurement == "temperature")
              |> max(column:"_value")

        '''

        min_result = influx_client.query_api().query(
            org=settings.INFLUXDB_ORG, query=q_min)
        max_result = influx_client.query_api().query(
            org=settings.INFLUXDB_ORG, query=q_max)
        
        print(min_result)
        print(max_result)
        print(f"\n\nMIN_Q: {q_min}")
        print(f"\n\nMAX_Q: {q_max}")

        if (min_result == [] or min_result == [] ):
            return TemperatureStatistics(
            min=0, max=0, valid=False)

     
        print(f"\n\n{min_result[0]}\n\n")
        print(f"\n\n{max_result[0]}\n\n")
        return TemperatureStatistics(
            min=min_result[0].records[0]["_value"], max=max_result[0].records[0]["_value"], valid=True)


schema = graphene.Schema(query=Query)
