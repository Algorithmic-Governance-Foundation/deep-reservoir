from enum import Enum
from typing import List
from attrs import define


class Status(Enum):
    YES = "YES"
    NO = "NO"
    PARTIAL = "PARTIAL"
    UNKNOWN = "UNKNOWN"


@define
class Result:
    policy: str
    country: str
    status: Status
    explanation: str
    sources: List[str]
    dump: str
    
    def __repr__(self) -> str:
        return f"Result(answer={self.status!r}, note={self.explanation!r})"
