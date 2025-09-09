from abc import ABC, abstractmethod

from deep_reservoir.result import Research


class Researcher(ABC):
    @abstractmethod
    def research(self, country: str, policy: str) -> Research:
        pass
