from utils import *
from rotors import *
from reflector import *
from plugboard import *
from enigma import *


########
# UTILS
########

def test_utils_read_rotors_1():
    assert read_rotors('rotors/I.rot') == [1] * 26

def test_utils_read_rotors_2():
    print read_rotors('rotors/V.rot')
    assert read_rotors('rotors/V.rot') == (
        [3, 23, 25, 1, 12, 14, 8, 16, 9, 20, 5, 4, 17, 
        21, 6, 18, 2, 11, 22, 24, 13, 19, 0, 10, 7, 15] )

def test_utils_read_plugboard1():
    assert read_plugboards('plugboards/I.pb') == [[25, 8]]

def test_utils_read_plugboard2():
    assert read_plugboards('plugboards/V.pb') == (
        [[21, 1], [24, 16], [10, 6], [14, 3], [0, 18], [20, 9], [4, 19],
         [2, 25], [7, 12], [5, 11], [15, 17], [8, 13], [23, 22]] )

def test_utils_read_null_plugboard():
    plugboard = Plugboard('plugboards/null.pb')
    assert plugboard.encode(7) == 7

def test_utils_read_null_plugboard_returns_empty_array():
    plugboard = Plugboard('plugboards/null.pb')
    assert plugboard.config_file == []


############
# PLUGBOARD
############

def test_plugboard_encode_1():
    plugboard = Plugboard('plugboards/I.pb')
    assert plugboard.encode(25) == 8

def test_plugboard_encode_2():
    plugboard = Plugboard('plugboards/I.pb')
    assert plugboard.encode(4) == 4

def test_plugboard_decode_1():
    plugboard = Plugboard('plugboards/I.pb')
    assert plugboard.decode(8) == 25


#########
# ROTORS
#########

def test_rotor_test_file_has_26_elements():
    assert len(read_rotors('rotors/I.rot')) == LETTERS_IN_ALPHABET

def test_rotor_encode_single_rotor_1():
    rotor = Rotor('rotors/I.rot')
    assert rotor.encode(0) == 1  # A -> B

def test_rotor_encode_single_rotor_2():
    rotor = Rotor('rotors/I.rot')
    assert rotor.encode(25) == 0  # Z -> A

def test_rotor_encode_two_rotors():
    rotor1 = Rotor('rotors/I.rot')
    rotor2 = Rotor('rotors/I.rot')
    assert rotor2.encode(rotor1.encode(0)) == 2

def test_rotor_decode_1():
    rotor = Rotor('rotors/I.rot')
    assert rotor.decode(0) == 25  # A -> Z

def test_rotor_decode_2():
    rotor = Rotor('rotors/I.rot')
    assert rotor.decode(1) == 0  # B -> A

def test_rotor_decode_3():
    rotor = Rotor('rotors/IV.rot')
    assert rotor.decode(18) == 0  # B -> A

def test_rotor_decode_opposite_to_encode_1():
    rotor = Rotor('rotors/III.rot')
    assert rotor.decode(rotor.encode(5)) == 5

def test_rotor_decode_opposite_to_encode_2():
    rotor = Rotor('rotors/V.rot')
    assert rotor.decode(rotor.encode(16)) == 16

def test_rotor_rotation_changes_rotor_config_file():
    rotor = Rotor('rotors/I.rot')
    rotor.rotate()
    assert rotor.config == range(2,LETTERS_IN_ALPHABET)+[0,1]

def test_rotor_rotates_next_after_full_rotation():
    rotor = Rotor('rotors/I.rot')
    for _ in xrange(25):
        assert rotor.rotate() == False  # rotate 25 times
    assert rotor.rotate() == True

def test_rotor_rotates_next_twice_after_two_full_rotations():
    rotor = Rotor('rotors/I.rot')
    for _ in xrange(LETTERS_IN_ALPHABET-1):
        assert rotor.rotate() == False  # rotate 25 times
    assert rotor.rotate() == True  # should rotate next now
    for _ in xrange(LETTERS_IN_ALPHABET-1):
        assert rotor.rotate() == False  # another 25 times
    assert rotor.rotate() == True  # should rotate next again

def test_rotors_decode_is_opposite_to_encode_after_one_rotation():
    rotor1 = Rotor('rotors/I.rot')
    rotor2 = Rotor('rotors/II.rot')
    # read from inside out
    assert rotor1.decode(rotor2.decode(rotor2.encode(rotor1.encode(0)))) == 0
    rotor1.rotate()
    assert rotor1.decode(rotor2.decode(rotor2.encode(rotor1.encode(0)))) == 0


############
# REFLECTOR
############

def test_reflector_encode_1():
    reflector = Reflector(15)
    assert reflector.encode(0) == 15

def test_reflector_encode_2():
    reflector = Reflector(3)
    assert reflector.encode(24) == 1


def test_reflector_decode_1():
    reflector = Reflector(15)
    assert reflector.decode(15) == 0

def test_reflector_decode_2():
    reflector = Reflector(3)
    assert reflector.decode(1) == 24

def test_reflector_decode_opposite_to_encode():
    reflector = Reflector(17)
    assert reflector.decode(reflector.encode(5)) == 5


#################
# ENIGMA MACHINE
#################

# Try to do this with mocks later so
# test cases don't rely on other
# implementations

# from mock import MagicMock

# Reflector implementation tests
def test_enigma_encodes_message_correctly_with_just_reflector():
    enigma = EnigmaMachine('plugboards/null.pb')
    assert enigma.encode_message('ABCDEFGHIJKLMNOPQRSTUVWXYZ') == 'NOPQRSTUVWXYZABCDEFGHIJKLM'

# Plugboard implementation tests
def test_enigma_encodes_message_correctly_with_just_plugboard_1():
    enigma = EnigmaMachine('plugboards/I.pb')
    assert enigma.encode_message('ABCDEFGHIJKLMNOPQRSTUVWXYZ') == 'NOPQRSTUMWXYIABCDEFGHZJKLV'

def test_enigma_encodes_message_correctly_with_just_plugboard_2():
    enigma = EnigmaMachine('plugboards/II.pb')
    assert enigma.encode_message('ABCDEFGHIJKLMNOPQRSTUVWXYZ') == 'NOPQISTUEWMYKABCDVFGHRJZLX'

# Basic rotor tests
def test_enigma_encodes_message_correctly_with_one_rotor_basic_1():
    enigma = EnigmaMachine('rotors/I.rot', 'plugboards/null.pb')
    assert enigma.encode_message('AAAAAAAAAAAAAAAAAAAAAAAAAA') == 'NNNNNNNNNNNNNNNNNNNNNNNNNN'

def test_enigma_encodes_message_correctly_with_one_rotor_basic_2():
    enigma = EnigmaMachine('rotors/II.rot', 'plugboards/null.pb')
    assert enigma.encode_message('AAAAAAAAAAAAAAAAAAAAAAAAAA') == 'PLPLPLPLPLPLPLPLPLPLPLPLPL'

# Complex rotor tests
def test_enigma_encodes_message_correctly_with_one_rotor_complex_single_letter():
    enigma = EnigmaMachine('rotors/V.rot', 'plugboards/null.pb')
    assert enigma.encode_message('A') == 'L'

def test_enigma_encodes_message_correctly_with_one_rotor_complex_1():
    enigma = EnigmaMachine('rotors/V.rot', 'plugboards/null.pb')
    assert enigma.encode_message('AAAAAAAAAAAAAAAAAAAAAAAAAA') == 'LLFORJEVOKWPPKRFJMGQVJMQUR'

def test_enigma_encodes_message_correctly_with_one_rotor_complex_2():
    enigma = EnigmaMachine('rotors/V.rot', 'plugboards/null.pb')
    assert enigma.encode_message('DDDDDDDDDDDDDDDDDDDDDDDDDD') == 'KYRVLIQWULYGVOAGPVAQGLIASM'

def test_enigma_encodes_message_correctly_with_one_rotor_complex_3():
    enigma = EnigmaMachine('rotors/V.rot', 'plugboards/null.pb')
    assert enigma.encode_message('KLKLKLKLKLKLKLKLKLKLKLKLKL') == 'PKJSRUTBANMJIWVSRNMJISRVUQ'

# Rotor cascade tests
def test_enigma_encodes_message_with_rotor_cascade_1():
    enigma = EnigmaMachine('rotors/I.rot', 'rotors/II.rot', 'plugboards/null.pb')
    assert enigma.encode_message('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA') == 'LLLLLLLLLLLLLLLLLLLLLLLLLLPPPPPPPPPPPPPPPPPPPPPPPPPP'

















