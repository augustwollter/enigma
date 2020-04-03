import enigma
import numpy as np
message = 'dearmisterknowitall'
print(message)
m = enigma.mword(message)

r = enigma.mrot(4)
m = np.matmul(r,m)
word = enigma.word(m)
print(word)
r2 = enigma.mrot(-4)
m = np.matmul(r2,m)
word2 = enigma.word(m)
print(word2)

a = enigma.Message('aoeu')
print(a)
