from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import time, sys

# inspired by https://pycryptodome.readthedocs.io/en/latest/src/cipher/oaep.html

KEY_SIZE = 2048

def generate_key_pair(id):
    private_key = RSA.generate(KEY_SIZE)
    public_key = private_key.public_key()
    
    # export key pair
    pub_key_file = f'{id}_public_key.pub'
    pri_key_file = f'{id}_private_key.pri'
    with open(pub_key_file, 'wb') as f:
        f.write(public_key.export_key())
    with open(pri_key_file, 'wb') as f:
        f.write(private_key.export_key())
    return pub_key_file, pri_key_file

def encrypt(plaintext, public_key_file):
    # plaintext must be plain string, not bytes
    try:
        start = time.time()
        key = RSA.import_key(open(public_key_file, 'rb').read())
        cipher = PKCS1_OAEP.new(key)
        ciphertext_byte = cipher.encrypt(plaintext.encode('utf-8'))
        end = time.time()
        print(f'Encryption time: {end - start}')
        return base64.b64encode(ciphertext_byte).decode('utf-8')
    except FileNotFoundError:
        print('public key not found')
    except ValueError:
        print('the message is too long, exceeding 190 bytes')

def decrypt(ciphertext, private_key_file):
    # ciphertext must be text string, not bytes
    try:
        start = time.time()
        key = RSA.import_key(open(private_key_file, 'rb').read())
        cipher = PKCS1_OAEP.new(key)
        plaintext_byte = cipher.decrypt(base64.b64decode(ciphertext))
        end = time.time()
        print(f'Decryption time: {end - start}')
        return plaintext_byte.decode('utf-8')
    except FileNotFoundError:
        print('private key not found')

def main():
    pub_file, pri_file = generate_key_pair('Alice')
    plaintext_file = sys.argv[1]

    ciphertext = encrypt(open(plaintext_file, 'r').read(), pub_file)
    decrypted_text = decrypt(ciphertext, pri_file)

    print(f'Ciphertext: {ciphertext}')
    print(f'Plaintext: {decrypted_text}')

if __name__ == '__main__':
    main()