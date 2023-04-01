from abc import ABC, abstractmethod


class ITrain(ABC):
    @abstractmethod
    def read_all(self):
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def delete(self):
        pass
