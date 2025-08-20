from abc import ABC, abstractmethod

from deep_reservoir.result import Result


class Researcher(ABC):
    @abstractmethod
    def go(self, prompt: str) -> Result:
        pass
