from utils import read_rotors, LETTERS_IN_ALPHABET
from encoder import Encoder

class Rotor(Encoder):

    def __init__(self, config_file):
        self.config_encode, self.config_decode = read_rotors(config_file)
        self.rotation_count = 0

    def encode(self, input):
        return (input + self.config_encode[input]) % 26  # return output

    def decode(self, output):
        return (output + self.config_decode[output]) % 26  # return input

    def rotate(self):
        self.config_encode = self.config_encode[1::] + [self.config_encode[0]] # anti-clockwise
        self.config_decode = self.config_decode[1::] + [self.config_decode[0]] # anti-clockwise
        self.rotation_count += 1
        if self.rotation_count % LETTERS_IN_ALPHABET == 0:
            return True  # full rotation
        else:
            return False