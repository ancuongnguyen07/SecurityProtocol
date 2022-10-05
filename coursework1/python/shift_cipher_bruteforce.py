import string

ALPHABET = string.ascii_uppercase
N = len(ALPHABET)

def decrypt(ciphertext, shift_key):
    plaintext = []
    for ch in ciphertext.upper():
        index = ALPHABET.find(ch)
        if index == -1:
            plaintext.append(ch)
            continue
        new_index = (index + shift_key) % N
        plaintext.append(ALPHABET[new_index])
    return ''.join(plaintext) 

ciphertext = 'AQW JCXG TGCEJGF C PGY NGXGN - CFOKP'
for key in range(N):
    plaintext = decrypt(ciphertext, key)
    print(f'Shift key {key}: {plaintext}')