from enum import Enum
from typing import List
from attrs import define


class Status(str, Enum):
    YES = "YES"
    NO = "NO"
    PARTIAL = "PARTIAL"
    UNKNOWN = "UNKNOWN"


@define
class Research:
    policy: str
    country: str
    data: str


@define
class Summary:
    status: Status
    explanation: str
    sources: List[str]
    dump: str
