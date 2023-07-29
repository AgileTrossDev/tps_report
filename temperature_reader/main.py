#!/usr/bin/env python3

import os
import time
from influxdb_client import InfluxDBClient


class TemperatureInfluxDbReader:

    def __init__(self) -> None:
        """
        Set your InfluxDB credentials and connection details
        """

        influxdb_url = os.environ.get(
            'INFLUXDB_DB_URL', 'http://localhost:8086')
        influxdb_token = os.environ.get(
            'DOCKER_INFLUXDB_INIT_ADMIN_TOKEN', 'my-admin-token')
        self.influxdb_org = os.environ.get(
            'DOCKER_INFLUXDB_INIT_ORG', 'my-org')
        self.influxdb_bucket = os.environ.get(
            'DOCKER_INFLUXDB_INIT_BUCKET', 'my-bucket')

        # Create the InfluxDB client
        print(
            f"TemperatureInfluxDbReader connect to InfluxDB URL: {influxdb_url}")
        self.client = InfluxDBClient(url=influxdb_url, token=influxdb_token)
        self.active = True

    def disconnect(self):
        """
        Closes connection and goes inactive
        """
        self.client.close()
        print("Disconnected from Influx")
        self.active = False

    def read_temperature_measurement(self):
        """
        Query the "temperature" measurement
        """

        query = f'''
          from(bucket: "{self.influxdb_bucket}")
          |> range(start: -2s)
          |> filter(fn: (r) => r._measurement == "temperature")
        '''
        result = self.client.query_api().query(query, org=self.influxdb_org)

        # Print the temperature values
        for table in result:
            for record in table.records:
                print(
                    f"Temperature: {record['_time']} - Value: {record['_value']}")

    def execution_loop(self):
        """
        Query the "temperature" measurement every 2 seconds while active
        """
        while self.active:
            self.read_temperature_measurement()
            print("Waiting for 2 seconds...")
            time.sleep(2)


# Main Execution
if __name__ == "__main__":
    client = TemperatureInfluxDbReader()
    try:
        client.execution_loop()
    except KeyboardInterrupt:
        print("\nScript interrupted. Exiting...")
        client.disconnect()
