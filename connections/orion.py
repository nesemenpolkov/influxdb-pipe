import os 
import urllib3

from datetime import datetime, timedelta

import orionsdk 
import pandas as pd
import numpy as np

from utils.singleton import singleton
from utils.dto import L3VPNTrafficLoad

from config import Config

try:
    server = Config.orion_server
    name = Config.orion_username
    password = Config.orion_password
    port = Config.orion_port
    print("Loaded deployment configs")
except KeyError:
    server = "10.30.2.98"
    name = "yalovegin"
    password = "5p@ceMar1ne"
    port = 17778
    print("Loaded development configs")

ORION_EXCLUDE_PROTOCOLS = ["0", "46", "112"]
ORION_TIMEOUT = 480


@singleton
class OrionDB:
    def __init__(self, server: str, name: str, password: str, port: int = 17778):
        self.swis = orionsdk.SwisClient(hostname=server, username=name, password=password, port=port, verify=False)

        verify = False
        if not verify:
            from urllib3.exceptions import InsecureRequestWarning
            urllib3.disable_warnings(InsecureRequestWarning)

    def getInterface(self, series_length, interface_id):
        s = "Select TOP "
        s += str(series_length)
        s += " it.InterfaceID, it.DateTime, it.InAveragebps, it.OutAveragebps FROM Orion.NPM.InterfaceTraffic it where InterfaceID = "
        s += str(interface_id)
        s += " order by it.DateTime"
        
        results = self.swis.query(s)

        ins = list()
        insTrains = list()
        outs = list()
        outsTrains = list()
        itr = 0

        series_length = int(series_length)
        percentile = ((series_length / 5) * 4)

        for row in results['results']:
            
            if itr >= series_length:
                break
            if itr > percentile:
                insTrains.append(np.log(row['InAveragebps']))
                outsTrains.append(np.log(row['OutAveragebps']))
                itr += 1
                continue 
            ins.append(np.log(row['InAveragebps']))
            outs.append(np.log(row['OutAveragebps']))
            itr += 1

        return ins, insTrains, outs, outsTrains

    def get_latest(self, days: int, rd: str, dataclass: bool = True):
        data = self.get_vrf_traffic_load(rd, days)
        if not dataclass:
            data = pd.DataFrame(
                {
                    "TimeStamp": [item.timestamp for item in data],
                    "TotalBytes": [item.bytes for item in data]
                }
            )
        return data
    
    def get_vrf_traffic_load(
        self,
        rd: str = "",
        days: int = 1
        ) -> list[L3VPNTrafficLoad]:
        
        timestamp = datetime.now()
        paststamp = timestamp - timedelta(days=days)
        #  TOP {str(history)}
        q = f"""
        SELECT f.TimeStamp, SUM(f.Bytes) as TotalBytes
        FROM Orion.Netflow.FlowsByInterface f
        JOIN Orion.NPM.Interfaces i ON f.InterfaceID = i.InterfaceID
        JOIN Orion.Routing.VRFInterface vi ON i.InterfaceID = vi.Interface.InterfaceID
        WHERE 
        f.ProtocolID NOT IN ({','.join(ORION_EXCLUDE_PROTOCOLS)}) 
        AND f.SourceIP != '0.0.0.0'
        AND f.DestinationIP != '0.0.0.0'
        AND vi.VRF.RouteDistinguisher = '{rd}'
        AND f.TimeStamp > '{str(paststamp)}'
        AND f.TimeStamp <= '{str(timestamp)}'
	    GROUP BY f.TimeStamp
	    ORDER BY f.TimeStamp
    """
        print(q)

        traffic = list()
        for t in self.swis.query(q, timeout=ORION_TIMEOUT).get("results"):
            traffic.append(
                L3VPNTrafficLoad(
                    timestamp=t["TimeStamp"], total_bytes=int(t["TotalBytes"]), rd=rd
                )
            )
        return traffic
    

orion_conn = OrionDB(server, name, password, port)
