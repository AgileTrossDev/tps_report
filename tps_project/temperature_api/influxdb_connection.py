from influxdb_client import InfluxDBClient
from tps_project import settings

# Replace with your InfluxDB configuration
# TODO: Pull from environment
# INFLUXDB_URL = "http://localhost:8086"
# INFLUXDB_TOKEN = "my-admin-token"
# INFLUXDB_ORG = "my-org"
# INFLUXDB_BUCKET = "my-bucket"
# settings.INFLUXDB_URL
# settings.INFLUXDB_ORG
# settings.INFLUXDB_TOKEN
# settings.INFLUXDB_BUCKET


def get_influxdb_client():
    # TODO: Consider using a Connection Pool
    return InfluxDBClient(url=settings.INFLUXDB_URL,
                          token=settings.INFLUXDB_TOKEN)
