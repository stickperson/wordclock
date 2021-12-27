from abc import ABC, abstractmethod


class BaseDisplay(ABC):
    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def update_position(self, position, *args, **kwargs):
        pass

    @abstractmethod
    def batch_update(self, words, **kwargs):
        pass

    @abstractmethod
    def display(self):
        pass

    @abstractmethod
    def wheel(self, idx):
        pass

    @abstractmethod
    def cleanup(self):
        pass
