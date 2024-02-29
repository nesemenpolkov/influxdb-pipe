import time
from dataclasses import dataclass

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from utils.singleton import singleton
from config import Config


# token = "VA4n9UqcFEqlR5i23shRMDBRGbgKmwx5gCzdvUPkC7qZfBzUDZwH6aeHjySTNK3tvpFDMkxEnQ8zTc-AlL8HQg=="
# org = "FSONET"
# url = "http://10.30.2.11:8088"

# client = InfluxDBClient(url=url, token=token, org=org)

# bucket="lol"

# write_api = client.write_api(write_options=SYNCHRONOUS)
# write_api.write()
   
# for value in range(5):
#   point = (
#     Point("with-time")
#     .tag("tagname1", "tagvalue1")
#     .field("field1", value)
#     .time(time=datetime.utcnow())
#   )
#   write_api.write(bucket=bucket, org="FSONET", record=point)
#   time.sleep(1) # separate points by 1 second


#    write_api.write(bucket="my-bucket",
#                     record=sensor,
#                     record_measurement_key="name",
#                     record_time_key="timestamp",
#                     record_tag_keys=["location", "version"],
#                     record_field_keys=["pressure", "temperature"])

class InfluxDBConnection:
    def __init__(self, url, org, token, bucket, structure_template = None):
        self.conn = InfluxDBClient(url=url, token=token, org=org)
        self.bucket = bucket
        if structure_template is None:
           self.use_default_structure_template() # dataclass template

        self.write_conn = self.conn.write_api(write_options=SYNCHRONOUS)
        self.query_conn = self.conn.query_api()

    def use_default_structure_template(self):
        self.structure_template = {
           "record_measurement_key": "measure",
           "record_time_key": "timestamp",
           "record_tag_keys": ["rd"],
           "record_field_keys": ["total_bytes"]
        }

    def write_data(self, data: list[dataclass]):
        # for item in data:
        self.write_conn.write(
                bucket=self.bucket,
                record=data,
                record_measurement_name="Netflow",
                record_time_key="timestamp",
                record_tag_keys=["rd"],
                record_field_keys=["total_bytes"]
        )
        # time.sleep(1)

    def get_data_by_rd_and_history(self, rd: str, history: int):
        pass


try:
    influx_conn = InfluxDBConnection(
        Config.influx_url,
        Config.influx_org,
        Config.influx_token,
        Config.influx_bucket
    )
except:
    influx_conn = InfluxDBConnection(
        "http://10.30.2.11:8088",
        "FSONET",
        "VA4n9UqcFEqlR5i23shRMDBRGbgKmwx5gCzdvUPkC7qZfBzUDZwH6aeHjySTNK3tvpFDMkxEnQ8zTc-AlL8HQg==",
        "orion"
    )