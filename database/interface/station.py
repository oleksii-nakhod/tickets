from abc import ABC, abstractmethod


class IStation(ABC):
    @abstractmethod
    def read_all(self):
        pass

    @abstractmethod
    def read(self):
        pass
