from abc import ABC, abstractmethod


class ITrain(ABC):
    @abstractmethod
    def read_all(self):
        pass

    @abstractmethod
    def read(self):
        pass
