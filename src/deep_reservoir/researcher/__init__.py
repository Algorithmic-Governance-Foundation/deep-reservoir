from abc import ABC, abstractmethod

from ..result import Result


class Researcher(ABC):
    @abstractmethod
    def go(self, country: str, policy: str) -> Result:
        pass
