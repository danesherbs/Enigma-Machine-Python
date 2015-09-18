from utils import read_rotors, LETTERS_IN_ALPHABET
from encoder import Encoder

class Rotor(Encoder):

    def __init__(self, config_file):
        self.config = read_rotors(config_file)
        self.rotation_count = 0

    def encode(self, input):
        return self.config[input]  # return output

    def decode(self, output):
        return self.config.index(output)  # return input

    def rotate(self):
        self.config = self.config[1::] + [self.config[0]] # anti-clockwise
        self.rotation_count += 1
        if self.rotation_count % LETTERS_IN_ALPHABET == 0:
            return True  # full rotation
        else:
            return False