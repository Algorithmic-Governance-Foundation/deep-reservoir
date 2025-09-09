from abc import ABC, abstractmethod

from deep_reservoir.result import Research, Summary


class Summariser(ABC):
    @abstractmethod
    def summarise(self, research: Research) -> Summary:
        pass
