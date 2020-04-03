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
    #rot *= -1
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
    """
    Creates a permutation matrix for combinations of permutations, given in a
    list of strings.
    """
    matrix = np.identity(26, dtype = 'int')
    
    for cycle in list_of_cycles:
        cpm = cyclic_permutation_matrix(cycle)
        np.matmul(cpm, matrix, out = matrix)

    return matrix


class Message():
    """
    Class for messages to encrypt and decrypt.
    """
    def __init__(self, word):
        """
        Create message object from string
        """
        self.matrix = word_to_matrix(word)

    def __str__(self):
        return matrix_to_word(self.matrix)
    
    def __repr__(self):
        return f"Message: {self.__str__()}"

    def transform(self, t, pos):
        """
        Perform a given transformation on the letter in the message at a 
        specific position
        """
        self.matrix[:,pos] = np.matmul(t.getTransform(), self.matrix[:,pos])
    def inverseTransform(self, t, pos):
        """
        Perform the inverse of a given transformation on the letter in the 
        message at a specific position
        """
        self.matrix[:,pos] = np.matmul(t.getInverseTransform(), self.matrix[:,pos])

class Transform():
    """
    Base class for different transformations
    """
    def __init__(self, matrix = np.identity(26, dtype = "int")):
        self.matrix = matrix

    def __repr__(self):
        return "Transformation"

    def getTransform(self):
        """
        matrix representation of the transformation
        """
        return self.matrix

class Rotation(Transform):
    """
    A class to create a rotation in the alphabet, like a ceasar cipher
    (unused by the project, created as a test)
    """
    def __init__(self, rot):
        self.matrix = rotation_matrix(rot)
        self.rot = rot % 26

    def __repr__(self):
        return f"Rotation by {self.rot}"

class Rotor(Transform):
    """
    Class for the Rotors
    """
    def __init__(self, permutation_matrix, pos, notch):
        """
        Creates a rotor with a given permutation matrix, at a specific position
        with the notch determined
        """
        self.permutation_matrix = permutation_matrix
        self.pos = pos
        self.original_pos = pos
        self.notch = notch
        
    def getTransform(self):
        """
        Get the transformation matrix
        """
        # the matrix is created when it is called
        matrix = np.matmul(rotation_matrix(self.pos), self.permutation_matrix)
        return matrix

    def getInverseTransform(self):
        """
        Get the inverse transformation matrix
        """
        return self.getTransform().T
    
    def __repr__(self):
        return f"Rotor at pos:{self.pos} and notch:{self.notch}"
    
    def step(self):
        """
        Steps the rotor forward
        """
        self.pos = (self.pos + 1) % 26

    def checkNotch(self):
        """
        Returns true if the Rotor is in its notch position
        """
        return (self.pos == self.notch)

    def reset(self):
        """
        Resets the rotor to initial position
        """
        self.pos = self.original_pos

class Reflector(Transform):
    """
    Class for the reflector
    """
    def __init__(self, list_of_cycles):
        self.list_of_cycles = list_of_cycles
        self.matrix = list_cyclic_permutation_matrix(list_of_cycles)
        
    def getTransform(self):
        return self.matrix # Never steps

    def getListOfCycles(self):
        return self.list_of_cycles


class Machine():
    """
    Class representing an enigma machina
    """
    def __init__(self, rotors, reflector):
        """
        Create a new machine with a list of Rotor objects, and a Reflector.

        Supports machines with varying number of Rotors
        """
        self.rotors = rotors
        self.reflector = reflector

    def __repr__(self):
        return str(self.components)
    
    def reset(self):
        """
        Reset rotors to initial positions
        """
        for r in self.rotors:
            r.reset()
    
    def transformMessage(self, message):
        """
        encrypts the message
        """
        # Iterate through each of the letters
        for i in range(message.matrix.shape[1]):
            # iterate forwards through the rotors
            for r in self.rotors:
                message.transform(r, i)
            # through the reflector
            message.transform(self.reflector, i)
            # and backwards through the rotors again,
            # in reverse order and with inverse transforms
            for r in reversed(self.rotors):
                message.inverseTransform(r, i)
            # Step the first rotor forward everytime
            self.rotors[0].step()
            # Check the other rotors if, the rotor before is in its notch
            # if so: step it!
            for i in range(len(self.rotors)-1,  0, -1):
                if (self.rotors[i-1].checkNotch()):
                    self.rotors[i].step()
                  
        return message


        
