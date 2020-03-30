import numpy as np

cipher = np.arange(26)
print(cipher)
cipher = (cipher + 2) % 26
print(cipher)
print(cipher[3])


def transformCharToNum(character):
    """
    Transform from unicode to a = 0, z = 25 letter representation
    """
    if (len(character) > 1):
        raise TypeError(f"Expected a character, but string of length {len(character)} found")
    # Unicode 
    num = ord(character)
    if ((num < 97) | (num > 122)):
        raise TypeError(f"Expected a letter a-z, but character is {character}")
    # a = 0
    num -= 97
    return int(num)
def transformNumToChar(Num):
    """
    Transforms int(a = 0, z = 25) to string character
    """
    # to Unicode
    char = chr(Num + 97)
    return char

def transformWordToNum(word):
    """
    Transform word to array of numbers
    """
    if not (isinstance(word,str)):
        raise TypeError(f"Expected a string")
    
    num_word = np.zeros(len(word),'int32')
    for i in range(len(word)):
        num_word[i] = transformCharToNum(word[i])

    return num_word

def transformNumToWord(num):
    """
    Transform array of numbers to words
    """
    word = ''
    for i in num:
        word += transformNumToChar(i)
    return word

def ceasarEncrypt(word, offset):
    return (word+offset) % 26
    
print(transformWordToNum('abcdef'))
print(transformWordToNum('august'))
        

