from dataclasses import dataclass
from datetime import datetime


@dataclass
class L3VPNTrafficLoad:
    timestamp: datetime = str(datetime.now())
    total_bytes: float = 1
    rd: str = "65000:20"
    measure: str = "Netflow"