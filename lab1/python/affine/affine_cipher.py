import string, sys

ALPHABET = string.ascii_uppercase
KEY_SPACE = len(ALPHABET)

INVERSE_TABLE = {
    1: 1, 3: 9, 5: 21,
    7: 15, 9: 3, 11: 19,
    15: 7, 17: 23, 19: 11,
    21: 5, 23: 17, 25: 25
}

def is_prime(a):
    for i in range(2,a//2):
        if a % i == 0:
            return False
    return True

def encryption(plaintext, a, b):
    if not is_prime(a):
        raise ValueError('a must be a prime')

    ciphertext = []
    for letter in plaintext.upper():
        index = ALPHABET.find(letter)
        if index == -1:
            ciphertext.append(letter)
            continue

        new_index = (a * index + b) % KEY_SPACE
        ciphertext.append(ALPHABET[new_index])
    
    return ''.join(ciphertext)

def decryption(ciphertext, a, b):
    if not is_prime(a):
        raise ValueError('a must be a prime')

    plaintext = []
    for letter in ciphertext.upper():
        index = ALPHABET.find(letter)
        if index == -1:
            plaintext.append(letter)
            continue

        c = INVERSE_TABLE[a]
        new_index = c * (index - b) % KEY_SPACE
        plaintext.append(ALPHABET[new_index])
    return ''.join(plaintext)

def main():
    mode = int(sys.argv[1])
    text,a,b = sys.argv[2:5]
    a,b = int(a), int(b)

    try:
        if mode == 1:
            # encryption mode
            result = encryption(text, a, b)
        else:
            # decryption mode
            result = decryption(text, a, b)
        print(f'Result: {result}')
    except:
        print('ERROR')

if __name__ == '__main__':
    main()