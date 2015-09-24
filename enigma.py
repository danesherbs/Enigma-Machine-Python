from encoder import Encoder
from rotors import Rotor
from plugboard import Plugboard
from reflector import Reflector

class EnigmaMachine(Encoder):

    def __init__(self, *configs):
        self.plugboard = Plugboard(configs[-1])

        self.rotors = []  # initially no rotors
        for rotor_path in configs[:-1]:
            self.rotors.append(Rotor(rotor_path))

        self.reflector = Reflector(13)

    def encode(self, input):
        input = ord(input) - ord('A')  # A -> 0, ..., Z -> 25
        output = self.plugboard.encode(input)
        output = self.pass_rotors('encode', output)
        output = self.reflector.encode(output)
        output = self.pass_rotors('decode', output)
        output = self.plugboard.decode(output)

        if len(self.rotors) > 0:  # check for rotors
            self.rotate_rotors(0)  # rotate necessary rotors
        return chr(output + ord('A'))

    def encode_message(self, message):
        encoded_message = ''
        for letter in message:
            if letter == ' ':
                encoded_message += ' '
            else:
                encoded_message += self.encode(letter)
        return encoded_message

    def decode(self, output):
        return self.encode(output)  # reciprocal cipher

    def rotate_rotors(self, rotor_i):
        if self.rotors[rotor_i].rotate():
            rotor_i += 1
            if rotor_i < len(self.rotors):
                self.rotate_rotors(rotor_i)

    def pass_rotors(self, transformer, input):
        direc = -1 if transformer == 'decode' else 1
        for rotor_num, rotor in enumerate(self.rotors[::direc]):
            # get output of current rotor
            if transformer == 'encode':
                input = rotor.encode(input)
            else:  # decode
                input = rotor.decode(input) 
        return input










