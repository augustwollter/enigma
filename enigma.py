import numpy as np

def word_to_matrix(word):
    """
    transforms word to matrix representation mword
    """
    matrix = np.zeros((26, len(word)), dtype = "int")
    for i in range(len(word)):
        place = ord(word[i]) - 97
        if not ((place >= 0) and (place <= 26)):
            raise Exception('Only letters a-z allowed')
        matrix[place, i] = 1

    return matrix

def matrix_to_word(matrix):
    """
    transform mword to word
    """
    l = np.hsplit(matrix, matrix.shape[1])
    numbers = np.zeros(matrix.shape[1])
    for i in range(matrix.shape[1]):
        numbers[i] = int(l[i].argmax())

    numbers += 97
    word = ''
    for n in numbers:
        word += chr(int(n))
        
    return word

def rotation_matrix(rot):
    """
    Creates a rotation matrix (26,26) that shifts columns forwards or back
    """
    rot *= -1
    matrix = np.zeros((26,26), dtype = "int")
    indeces = (np.arange(26) + rot) % 26
    matrix[np.arange(26),indeces] = 1
    return matrix

def cyclic_permutation_matrix(cycle):
    """
    Creates a permutation matrix that shifts letters, dependent on the 
    cycle of letters given. 'abc' shift a->b, b->c, c->a, and leaves d-z
    untouched.
    """
    len_cycle = len(cycle)
    init = np.zeros(len_cycle, dtype = "int")
    target = np.zeros(len_cycle, dtype = "int")
    for i in range(len_cycle):
        num = ord(cycle[i]) - 97
        init[i] = int(num)
        target[(i + 1) % len_cycle] = int(num)
    matrix = np.identity(26, dtype = "int")
    for i in range(len_cycle):
        matrix[init[i],init[i]] = 0
        matrix[init[i],target[i]] = 1
    return matrix

def list_cyclic_permutation_matrix(list_of_cycles):
    matrix = np.identity(26, dtype = 'int')
    
    for cycle in list_of_cycles:
        cpm = cyclic_permutation_matrix(cycle)
        np.matmul(cpm, matrix, out = matrix)

    return matrix


class Message():
    def __init__(self, word):
        self.matrix = word_to_matrix(word)

    def __str__(self):
        return matrix_to_word(self.matrix)
    
    def __repr__(self):
        return f"Message: {self.__str__()}"

    def transform(self, t):
        self.matrix = np.matmul(t.getTransform(), self.matrix)
    def split(self):
        split = np.hsplit(self.matrix, self.matrix.shape[1])
        return split

class Transform():
    def __init__(self, matrix = np.identity(26, dtype = "int")):
        self.matrix = matrix

    def __repr__(self):
        return "Transformation"

    def getTransform(self):
        return self.matrix

class Rotation(Transform):
    def __init__(self, rot):
        self.matrix = rotation_matrix(rot)
        self.rot = rot % 26

    def __repr__(self):
        return f"Rotation by {self.rot}"

class Rotor(Transform):
    def __init__(self, permutation_matrix, pos, notch):
        self.permutation_matrix = permutation_matrix
        self.pos = pos
        self.notch = notch
    def getTransform(self):
        matrix = np.matmul(rotation_matrix(self.pos), self.permutation_matrix)

        if (self.pos == self.notch):
            print("Next rotor is advanced")

        return matrix
    def __repr__(self):
        return f"Rotor at pos:{self.pos} and notch:{self.notch}"
    
    def step(self):
        self.pos = (self.pos + 1) % 26

    # Implement stepping

class Reflector(Transform):
    def __init__(self, list_of_cycles):
        self.list_of_cycles = list_of_cycles
        self.matrix = list_cyclic_permutation_matrix(list_of_cycles)
    def getTransform(self):
        return self.matrix, False # Never steps

    def getListOfCycles(self):
        return self.list_of_cycles


class Machine():
    def __init__(self, rotors, reflector):
        self.rotors = rotors
        self.reflector = reflector

    def __repr__(self):
        return str(self.components)
    
    
    #def transformMessage(self, message):
        
        # Transform through rotors one way
        # Reflect
        # Back through rotors
        # step wheel(s)
        
