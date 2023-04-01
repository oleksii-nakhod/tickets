from abc import ABC, abstractmethod

class IConnectionPool(ABC):
    @abstractmethod
    def add_connection(self):
        pass

    @abstractmethod
    def get_connection(self):
        pass
