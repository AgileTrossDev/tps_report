import websockets
import asyncio
import json
import signal
from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS

class ConsumerDbClient:

  def __init__(self):
    # Set your InfluxDB credentials and connection details
    database_url = "http://localhost:8086"    
    self.org = "my-org"
    token = "my-admin-token"
    self.bucket = "my-bucket"

    # Temperature Stream
    # TODO: Make Configurable
    self.source_uri = "ws://localhost:1000/graphql" 

    # Create the InfluxDB client
    self.client = InfluxDBClient(url=database_url, token=token)

    # Get the write API
    self.write_api = self.client.write_api(write_options=WriteOptions(batch_size=500, flush_interval=10_000, jitter_interval=2_000, retry_interval=5_000))

    # Instance is now considered active and ready to execute
    self.active = True

  def handle_interrupt(self, signum, frame):
    print("\nInterrupt received. Stopping the loop.")
    self.active = False

  def disconnect(self):  
    # Close the client
    self.client.close()

  def process_msg(self,data):
    # Log Incoming Temp
    print(data["payload"]["data"]["temperature"])
  
    # Build record
    data_points = [
        {
            "measurement": "temperature",
            "tags": {"device": "1"},
            "fields": {"value": data["payload"]["data"]["temperature"]},
        }
    ]

    # Write the data points to the InfluxDB database
    self.write_api.write(bucket=self.bucket, org=self.org, record=data_points)

  # Execution pool that opens async websocket connection to a server stream Temperature Data
  # As each data record is received, the message is processed
  async def capture_data(self):
      
      start = {
          "type": "start",
          "payload": {"query": "subscription { temperature }"}
      }
      
      async with websockets.connect(self.source_uri, subprotocols=["graphql-ws"]) as websocket:
        await websocket.send(json.dumps(start))
        while self.active:
            data = await websocket.recv()
            client.process_msg(json.loads(data))

      print("Gracefully exited capture_data execute loop...")
      self.disconnect()
      print("capture_data is complete!")

# Main Execution if running as a Script
if __name__ == "__main__":
  print("Launching Consumer Client")
  client = ConsumerDbClient()

  # Set up the signal handler for SIGINT (Ctrl+C)
  signal.signal(signal.SIGINT, client.handle_interrupt)
  

  asyncio.run(client.capture_data())
  print("Exiting!")
