from abc import ABC, abstractmethod

class BaseGenerator(ABC):
    @abstractmethod
    def generate_record(self):
        pass

    def generate_records(self, count: int):
        return [self.generate_record() for _ in range(count)]
