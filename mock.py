from datetime import datetime, timedelta

import pandas as pd

from utils.dto import L3VPNTrafficLoad


def get_mock_data():
    datas = []
    df = pd.read_csv("data.csv")

    for i, row in df.iterrows():
        datas.append(
            L3VPNTrafficLoad(
                timestamp=row["TimeStamp"],
                total_bytes=row["TotalBytes"]
            )
        )
    return datas
