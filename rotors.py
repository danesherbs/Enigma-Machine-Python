from utils import read_rotors, LETTERS_IN_ALPHABET
from encoder import Encoder

class Rotor(Encoder):

    def __init__(self, config_file):
        self.config_encode, self.config_decode = read_rotors(config_file)
        self.rotation_count = 0

    def encode(self, input):
        print "Input:", input
        print "Offset:", self.config_encode[input]
        print "After:", (input + self.config_encode[input]) % 26
        print
        return (input + self.config_encode[input]) % 26  # return output

    def decode(self, output):
        print "Before:", output
        print "Offset:", self.config_decode[output]
        print "After:", (output + self.config_decode[output]) % 26
        return (output + self.config_decode[output]) % 26  # return input

    def rotate(self):
        self.config_encode = self.config[1::] + [self.config[0]] # anti-clockwise
        self.config_decode = self.config[1::] + [self.config[0]] # anti-clockwise
        self.rotation_count += 1
        if self.rotation_count % LETTERS_IN_ALPHABET == 0:
            return True  # full rotation
        else:
            return False