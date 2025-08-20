from enum import Enum
from typing import List
from attrs import define


class Answer(Enum):
    YES = "YES"
    NO = "NO"
    PARTIAL = "PARTIAL"
    UNKNOWN = "UNKNOWN"


@define
class Result:
    answer: Answer
    note: str
    sources: List[str]
    dump: str
