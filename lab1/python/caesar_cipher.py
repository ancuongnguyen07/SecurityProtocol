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
        for letter in plaintext.lower():
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
        for letter in ciphertext.lower():
            index = ALPHABET.find(letter)
            # print(index)
            if index == -1:
                plaintext.append(letter)
                continue

            new_index = (index - key_shift) % KEY_SPACE
            plaintext.append(ALPHABET[new_index])
        return ''.join(plaintext)
    except:
        print('ERROR')
        return None 

def starter():
    '''
    Ask a user which mode he/she want (decrypt/encrypt)
    and take the input text (ciphertext/plaintext)
    
    return a user's selection
    '''

    mode = input('You want encrypt (1) or decrypt (2)? Type 1 or 2: ' )
    if mode != '1' and mode != '2':
        raise ValueError()
    text = input('Your ciphertext/plaintext: ')
    key = input('Your key_shift: ')
    
    return int(mode), text, int(key)

def main():
    mode, text, key_shift = starter()
    if mode == 1:
        start = time.time()
        result = encryption(text, key_shift)
        end = time.time()
    else:
        start = time.time()
        result = decryption(text, key_shift)
        end = time.time()

    print(f"Result: {result}")
    print(f'Executino time: {end - start}')

if __name__ == '__main__':
    main()
