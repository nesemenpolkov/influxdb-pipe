from datetime import datetime
import time

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


token = "CLvTdr5VmynQ011RT_soP5HUP45t_D49bebqJYFgMgL_GUTc7J0aEoFPBJI6VFgBTBkEDuuSc3Q-bfegNzmqcw=="
org = "FSONET"
url = "http://10.30.2.11:8088"

client = InfluxDBClient(url=url, token=token, org=org)

bucket="lol"

write_api = client.write_api(write_options=SYNCHRONOUS)
# write_api.write()
points = []   
for value in range(10):
  point = (
    Point("with-time")
    .tag("tagname1", "tagvalue1")
    .field("field1", value)
    .time(time=datetime.utcnow())
  )
  write_api.write(bucket=bucket, org="FSONET", record=point)
  time.sleep(1) # separate points by 1 second