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
    policy: str
    country: str
    answer: Answer
    note: str
    sources: List[str]
    dump: str
    
    def __repr__(self) -> str:
        return f"Result(answer={self.answer!r}, note={self.note!r})"
