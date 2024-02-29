import os


class Config:
    influx_url = os.environ["INFLUXDB_URL"]
    influx_org = os.environ["INFLUXDB_ORG"]
    influx_token = os.environ["INFLUXDB_TOKEN"]
    influx_bucket = os.environ["INFLUXDB_BUCKET"]
    influx_default_measure = os.environ["INFLUXDB_DEFAULT_MEASURE"]
    orion_server = os.environ["orion_server"]
    orion_username = os.environ["orion_username"]
    orion_password = os.environ["orion_password"]
    orion_port = os.environ["orion_port"]