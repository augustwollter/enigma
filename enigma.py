import numpy as np

def word_to_matrix(word):
    """
    transforms word to matrix representation mword
    """
    matrix = np.zeros((26, len(word)))
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
    matrix = np.zeros((26,26))
    indeces = (np.arange(26) + rot) % 26
    matrix[np.arange(26),indeces] = 1
    return matrix

class Message():
    def __init__(self, word):
        self.matrix = word_to_matrix(word)

    def __str__(self):
        return matrix_to_word(self.matrix)
    
    def __repr__(self):
        return f"Message: {self.__str__()}"

    def transform(self, t):
        self.matrix = np.matmul(t.matrix, self.matrix)

class Transform():
    def __init__(self):
        self.matrix = np.identity(26)

    def __repr__(self):
        return "Transformation"

class Rotation(Transform):
    def __init__(self, rot):
        self.matrix = rotation_matrix(rot)
        self.rot = rot % 26

    def __repr__(self):
        return f"Rotation by {self.rot}"
class Rotor(Transform):
    def __init__(self, pos, notch):
        self.pos = pos
        self.notch = notch
    def getTransform(self):
        matrix = rotation_matrix(self.pos)
        step = False
        if (self.pos == self.notch):
            print("next rotor is advanced")
            step = True
        self.pos = (self.pos + 1) % 26
        return matrix, step
    def __repr__(self):
        return f"Rotor at pos:{self.pos} and notch:{self.notch}"
