from abc import ABC, abstractmethod
from typing import Awaitable

from ..result import Result


class Researcher(ABC):
    @abstractmethod
    def go(self, country: str, policy: str) -> Result:
        pass
    
    @abstractmethod
    async def go_async(self, country: str, policy: str) -> Result:
        pass
