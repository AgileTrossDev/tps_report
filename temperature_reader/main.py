import time
from influxdb_client import InfluxDBClient

class TemperatureInfluxDbReader:
    
  def __init__(self) -> None:
      
    # Set your InfluxDB credentials and connection details
    influxdb_url = "http://localhost:8086"  # Replace with your InfluxDB URL
    influxdb_token = "my-admin-token"  # Replace with your InfluxDB token
    self.influxdb_org = "my-org"  # Replace with your organization
    self.influxdb_bucket = "my-bucket"  # Replace with your bucket name

    # Create the InfluxDB client
    self.client = InfluxDBClient(url=influxdb_url, token=influxdb_token)
    self.active = True

  # Close the client
  def disconnect(self):    
    self.client.close()
    print ("Disconnected from Influx")
    self.active = False

  # Query the "temperature" measurement
  def read_temperature_measurement(self):
    
    query = f'from(bucket: "{self.influxdb_bucket}") |> range(start: -2s) |> filter(fn: (r) => r._measurement == "temperature")'
    result = self.client.query_api().query(query, org=self.influxdb_org)

    # Print the temperature values
    for table in result:
        for record in table.records:
            print(f"Temperature: {record['_time']} - Value: {record['_value']}")


  # Query the "temperature" measurement every 2 seconds while active
  def execution_loop(self):
      while self.active:
        self.read_temperature_measurement()
        print("Waiting for 2 seconds...")
        time.sleep(2)

if __name__ == "__main__":
    client = TemperatureInfluxDbReader()
    try:
        client.execution_loop()
    except KeyboardInterrupt:
        print("\nScript interrupted. Exiting...")
        client.disconnect()
