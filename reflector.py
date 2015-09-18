from encoder import Encoder
from utils import LETTERS_IN_ALPHABET

class Reflector(Encoder):

    def __init__(self, shift):
        self.shift = shift

    def encode(self, input):
        return ( input + self.shift ) % LETTERS_IN_ALPHABET

    def decode(self, output):
        return ( output - self.shift ) % LETTERS_IN_ALPHABET