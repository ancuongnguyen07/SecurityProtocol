import string, time

ALPHABET = string.ascii_lowercase
KEY_SPACE = len(ALPHABET)

def is_valid_key(key_shift):
    if key_shift < 0 or key_shift >= KEY_SPACE:
        raise ValueError('Invalid key_shift, it must be '\
                        f'between 0 and {KEY_SPACE}')

def encryption(plaintext, key_shift):
    try:
        is_valid_key(key_shift)

        ciphertext = []
        for letter in plaintext:
            index = ALPHABET.find(letter)
            if index == -1:
                ciphertext.append(letter)
                continue

            new_index = (index + key_shift) % KEY_SPACE
            ciphertext.append(ALPHABET[new_index])
        return ''.join(ciphertext)
    except:
        print('ERROR')
        return None

def decryption(ciphertext, key_shift):
    try:
        is_valid_key(key_shift)

        plaintext = []
        for letter in ciphertext:
            index = ALPHABET.find(letter)
            if index == -1:
                plaintext.append(letter)
                continue

            new_index = (index - key_shift) % KEY_SPACE
            plaintext.append(ALPHABET[new_index])
        return ''.join(ciphertext)
    except:
        print('ERROR')
        return None 

def starter():
    '''
    Ask a user which mode he/she want (decrypt/encrypt)
    and take the input text (ciphertext/plaintext)
    
    return a user's selection
    '''

    

def main():

    start = time.time()

    end = time.time()
    print(f'Executino time: {end - start}')

if __name__ == '__main__':
    main()
