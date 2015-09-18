from abc import ABCMeta, abstractmethod

class Encoder:

    __metaclass__ = ABCMeta

    @abstractmethod
    def encode(self, input):
        pass  # implement this in concrete class

    @abstractmethod
    def decode(self, output):
        pass  # implement this in concrete class