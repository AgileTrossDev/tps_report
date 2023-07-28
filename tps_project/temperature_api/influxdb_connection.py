from influxdb_client import InfluxDBClient

# Replace with your InfluxDB configuration
# TODO: Pull from environment
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "my-admin-token"
INFLUXDB_ORG = "my-org"
INFLUXDB_BUCKET = "my-bucket"


def get_influxdb_client():
    return InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN)
