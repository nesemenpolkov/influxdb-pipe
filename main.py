import os

from dotenv import load_dotenv
load_dotenv()
from connections.influx import influx_conn
from connections.orion import orion_conn
from mock import get_mock_data


if __name__ == "__main__":
    load_dotenv()
    # print(os.environ)
    # data = orion_conn.get_latest(1, "65000:20")
    data = get_mock_data()
    influx_conn.write_data(data)
    print("success?")


