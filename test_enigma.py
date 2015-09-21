from utils import *
from rotors import *
from reflector import *
from plugboard import *
from enigma import *


########
# UTILS
########

def test_utils_read_rotors_1():
    assert read_rotors('rotors/I.rot') == ([1] * 26, [25] * 26)

def test_utils_read_rotors_2():
    assert read_rotors('rotors/V.rot') == (
        [3, 22, 23, 24, 8, 9, 2, 9, 1, 11, 21, 19, 5,
         8, 18, 3, 12, 20, 4, 5, 19, 24, 4, 13, 9, 16],
        [22, 2, 14, 23, 7, 5, 8, 17, 24, 25, 13, 6, 18,
         7, 17, 10, 17, 21, 23, 2, 15, 18, 22, 4, 21, 3] )

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

def test_rotor_read_rotor_returns_two_lists_of_len_26():
    assert len(read_rotors('rotors/I.rot')) == 2
    assert len(read_rotors('rotors/I.rot')[0]) == LETTERS_IN_ALPHABET
    assert len(read_rotors('rotors/I.rot')[1]) == LETTERS_IN_ALPHABET

def test_rotor_encode_single_rotor_1():
    rotor = Rotor('rotors/I.rot')
    assert rotor.encode(0) == 1  # moves one position clockwise

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
    assert rotor.decode(18) == 0

def test_rotor_decode_opposite_to_encode_1():
    rotor = Rotor('rotors/III.rot')
    assert rotor.decode(rotor.encode(5)) == 5

def test_rotor_decode_opposite_to_encode_2():
    rotor = Rotor('rotors/V.rot')
    assert rotor.decode(rotor.encode(16)) == 16

def test_rotor_rotation_changes_rotor_config_file():
    rotor = Rotor('rotors/V.rot')
    rotor.rotate()
    assert rotor.config_encode == (
        [22, 23, 24, 8, 9, 2, 9, 1, 11, 21, 19, 5, 8, 
        18, 3, 12, 20, 4, 5, 19, 24, 4, 13, 9, 16, 3] )
    assert rotor.config_decode == (
        [2, 14, 23, 7, 5, 8, 17, 24, 25, 13, 6, 18, 7, 
        17, 10, 17, 21, 23, 2, 15, 18, 22, 4, 21, 3, 22] )

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
    enigma = EnigmaMachine('rotors/III.rot', 'plugboards/null.pb')
    assert enigma.encode_message('A') == 'L'

def test_enigma_encodes_message_correctly_with_one_rotor_complex_1():
    enigma = EnigmaMachine('rotors/III.rot', 'plugboards/null.pb')
    assert enigma.encode_message('AAAAAAAAAAAAAAAAAAAAAAAAAA') == 'LLFORJEVOKWPPKRFJMGQVJMQUR'

def test_enigma_encodes_message_correctly_with_one_rotor_complex_2():
    enigma = EnigmaMachine('rotors/IV.rot', 'plugboards/null.pb')
    assert enigma.encode_message('DDDDDDDDDDDDDDDDDDDDDDDDDD') == 'KYRVLIQWULYGVOAGPVAQGLIASM'

def test_enigma_encodes_message_correctly_with_one_rotor_complex_3():
    enigma = EnigmaMachine('rotors/V.rot', 'plugboards/null.pb')
    assert enigma.encode_message('KLKLKLKLKLKLKLKLKLKLKLKLKL') == 'PKJSRUTBANMJIWVSRNMJISRVUQ'

# Rotor cascade tests
def test_enigma_encodes_message_with_rotor_cascade_1():
    enigma = EnigmaMachine('rotors/I.rot', 'rotors/II.rot', 'plugboards/null.pb')
    assert enigma.encode_message('A' * 52) == 'L' * 26 + 'P' * 26

def test_enigma_encodes_message_with_rotor_cascade_2():
    enigma = EnigmaMachine('rotors/I.rot', 'rotors/II.rot', 'plugboards/IV.pb')
    assert enigma.encode_message('A' * 52) == 'Z' * 26 + 'X' * 26

def test_enigma_encodes_message_with_rotor_cascade_3():
    enigma = EnigmaMachine('rotors/II.rot', 'rotors/II.rot', 'plugboards/null.pb')
    assert enigma.encode_message('ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ') \
                    == 'NSPURWTYVAXCZEBGDIFKHMJOLQROTQVSXUZWBYDAFCHEJGLINKPM'

def test_enigma_encodes_message_with_rotor_cascade_4():
    enigma = EnigmaMachine('rotors/II.rot', 'rotors/II.rot', 'plugboards/III.pb')
    assert enigma.encode_message('ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ') \
                    == 'NQLWRUTCKVIYUEBGFXDKMJHRPSROPSVQIWGZBCQAFYMEHGNXLVTJ'

def test_enigma_encodes_message_with_rotor_cascade_5():
    enigma = EnigmaMachine('rotors/VI.rot', 'rotors/IV.rot', 'plugboards/II.pb')
    assert enigma.encode_message('ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ') \
                    == 'MGDSBKVCZTGFAGSJKPFDIZGIGMFHLWODQOXBJBWIPZHQMCZUDJSN'













