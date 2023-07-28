# GraphQL Schema that works InfluxDB hosting the Temperature Data for the System.
#
# NOTE: Relies on influxdb_connection() to be establish database connection
#       because InfluxDb is not natively supported by Django.
#
import graphene
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


  # Override the 'resolve_id' method to use the custom primary key field as the 'pk' field
  def resolve_id(self, info):    
    return self.time
        

class Query(graphene.ObjectType):
    temperature_measurements = graphene.List(TemperatureMeasurementType, description="Last 2 Seconds of Temperature measurement.")

    def resolve_temperature_measurements(self, info):
        """ 
        Resolver that fetches last 2 seconds of temperature measurements from InfluxDB
        using the influxdb_connection module and return them as Django objects.        
        """
                
        # Get the influx client and perform query        
        influx_client = get_influxdb_client()        
        query = f'from(bucket: "{"my-bucket"}") |> range(start: -2s) |> filter(fn: (r) => r._measurement == "temperature")'        
        result = influx_client.query_api().query(query, org="my-org")

        print ("resolve_temperature_measurements")
        print (type(result))

        # Buld Return Object
        temperature_measurements =[]
        for table in result:
          for record in table.records:
            print(f"Temperature: {record['_time']} - Value: {record['_value']}")
            tmp = TemperatureMeasurementType() 
            tmp.time=record['_time']
            tmp.value=record['_value']
            
            temperature_measurements.append(tmp)
            
        print("We good?")
        return temperature_measurements
    


schema = graphene.Schema(query=Query)