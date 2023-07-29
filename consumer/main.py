import websockets
import asyncio
import json
import signal
import os
import time

from influxdb_client import InfluxDBClient, WriteOptions


class ConsumerDbClient:

    def __init__(self):
        """
        Constructor that creates instance and establishes connection to the websocket
        """

        # Set InfluxDB credentials and connection details
        database_url = os.environ.get(
            'INFLUXDB_DB_URL', 'http://localhost:8086')
        self.org = os.environ.get('DOCKER_INFLUXDB_INIT_ORG', 'my-org')

        token = os.environ.get(
            'DOCKER_INFLUXDB_INIT_ADMIN_TOKEN',
            'my-admin-token')
        
        self.bucket = os.environ.get(
            'DOCKER_INFLUXDB_INIT_BUCKET', 'my-bucket')
        
        self.print_temps = os.environ.get(
            'RUNTIME_ENVIRONMENT', 'local') != "DOCKER"

        # Temperature Stream
        self.source_uri = os.environ.get(
            'SOURCE_URI', "ws://localhost:1000/graphql")

        # Instance is now considered active and ready to execute
        self.active = True
        self.write_api = None
        self.client = None

        self.connect(database_url, token)

    # Create the InfluxDB client and the write API
    # TODO: Deeper diver into the configuration of the client.  Larger Flush
    # Intervales, appears to cause data to drop
    def connect(self, database_url: str, token: str):
        print(f'''Attempting to connect to the Influx DB"
              "at {database_url}''')
        self.client = InfluxDBClient(url=database_url, token=token)
        self.write_api = self.client.write_api(
            write_options=WriteOptions(
                batch_size=500,
                flush_interval=250,
                jitter_interval=2_000,
                retry_interval=5_000))
        print("Influx DB Connected!")

    # Signal Handler that gracefully stops execution
    def handle_interrupt(self, signum: int, frame: int):
        print("Interrupt received. Stopping the loop.")
        self.active = False

    def disconnect(self):
        # Close the client
        self.client.close()
        print("Influx Client disconnected")

    def process_msg(self, data: dict):        
        if self.print_temps:
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
        self.write_api.write(
            bucket=self.bucket,
            org=self.org,
            record=data_points)


    async def shutdown(self):
        self.active = False

    # Execution pool that opens async websocket connection to a server stream Temperature Data
    # As each data record is received, the message is processed
    async def capture_data(self):
        
        self.active = True

        # Subscription Request
        start = {
            "type": "start",
            "payload": {"query": "subscription { temperature }"}
        }

        while self.active:
            print(
                f"Attempting to connect to the temperature telemtry stream at websocket {self.source_uri}")
            try:
                async with websockets.connect(self.source_uri, subprotocols=["graphql-ws"]) as websocket:
                    await websocket.send(json.dumps(start))
                    print(
                        f"Websocket connection and subscription was succesful to URI: {self.source_uri}")
                    while self.active:                        
                        await asyncio.sleep(0)
                        try:
                            data = await websocket.recv()                             
                            self.process_msg(json.loads(data))
                        except websockets.ConnectionClosedOK:
                            print("WebSocket connection closed gracefully.")
                            break
                        except websockets.ConnectionClosedError as e:
                            print(
                                f"WebSocket connection closed with error: {e}")
                            break
                        except Exception as e:
                            print(f"Unexpected error occurred: {e}")
                            break
            except websockets.WebSocketException as e:
                print(f"WebSocket communication error: {e}")
            except Exception as e:
                print(
                    f"Unexpected error occurred outside the WebSocket loop: {e}")
                break            
            await asyncio.sleep(0)

        print("Gracefully exited capture_data execution loop...")
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
