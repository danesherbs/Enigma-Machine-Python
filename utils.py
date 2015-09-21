LETTERS_IN_ALPHABET = 26

def read_rotors(filename):
    file = open(filename, 'r')
    array = [int(x) for x in file.readline().strip().split(' ')]
    encode_array = [0] * 26
    decode_array = [0] * 26
    for i, val in enumerate(array):
        encode_array[i] = (val - i) % 26
        decode_array[val] = (i - val) % 26
    file.close()
    return encode_array, decode_array

def read_plugboards(filename):
    if filename == 'plugboards/null.pb':  # special case
        return []
    array = [int(x) for x in open(filename, 'r').readline().strip().split(' ')]
    return [list(x) for x in zip(array[::2], array[1::2])] 
    