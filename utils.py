LETTERS_IN_ALPHABET = 26

def read_rotors(filename):
    file = open(filename, 'r')
    array = [int(x) for x in file.readline().strip().split(' ')]
    for i, val in enumerate(array):
        array[i] = (val - i) % 26
    file.close()
    return array

def read_plugboards(filename):
    if filename == 'plugboards/null.pb':  # special case
        return []
    array = read_rotors(filename)  # array of even num of ints
    return [list(x) for x in zip(array[::2], array[1::2])] 
    