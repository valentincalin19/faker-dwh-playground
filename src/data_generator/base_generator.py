from abc import ABC, abstractmethod
from typing import Any


class BaseGenerator(ABC):
    @abstractmethod
    def generate_record(self) -> Any:
        pass

    def generate_records(self, count: int) -> list:
        return [self.generate_record() for _ in range(count)]
