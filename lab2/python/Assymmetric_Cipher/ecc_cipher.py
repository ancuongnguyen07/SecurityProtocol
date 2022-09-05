import ecies
import time, sys

# inspired by https://github.com/ecies/py

def generate_key_pair():
    ec_key = ecies.utils.generate_key()
    secret_key = ec_key.secret # bytes
    public_key = ec_key.public_key.format(True) # bytes
    return public_key, secret_key

def encrypt(plaintext, public_key):
    return ecies.encrypt(public_key, plaintext)

def decrypt(ciphertext, private_key):
    return ecies.decrypt(private_key, ciphertext)

def main():
    if len(sys.argv) != 2:
        print('missing plaintext file name or too much file names')
        return
    try:
        plaintext = open(sys.argv[1], 'rb').read()

        # key pair generation
        public_key, private_key = generate_key_pair()

        # encryption
        enc_start = time.time()
        ciphertext = encrypt(plaintext, public_key)
        enc_end = time.time()

        # decryption
        de_start = time.time()
        decrypted_text = decrypt(ciphertext, private_key)
        de_end = time.time()

        print(f'Encryption time: {enc_end - enc_start}')
        print(f'Decryption time: {de_end - de_start}')
        print(f'Ciphertext: {ciphertext}\n')
        print(f'Plaintext: {decrypted_text}')
    except FileNotFoundError:
        print('Plaintext file not found') 

if __name__ == '__main__':
    main()