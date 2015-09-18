from encoder import Encoder
from utils import read_plugboards

class Plugboard(Encoder):

    def __init__(self, config_file):
        self.config_file = read_plugboards(config_file)

    def encode(self, input):
        for pair in self.config_file:
            if input in pair:  # swapped by plugboard
                if input == pair[0]:
                    return pair[1]
                else:
                    return pair[0]
        return input  # input not swapped by plugboard

    def decode(self, output):
        return self.encode(output)  # symmetric operation