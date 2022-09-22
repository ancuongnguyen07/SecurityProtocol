import sys, random, hashlib, base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
sys.path.insert(0, '../../lab1/python/caesar')
from caesar_cipher import decryption

def key_exchange(p, g, a, b):
    A = g**a % p
    B = g**b % p
    s = A**b % p

    assert s == B**a % p

    print(f'A: {A}')
    print(f'B: {B}')
    print(f'S: {s}')

    return s

def guess_shared_key(p, g, A, B):
    b = None
    for i in range(46):
        if g**i % p == B:
            b = i
            print(b)
            break
    
    if b:
        return A**b % p
    return None

def generate_random_number():
    return random.randint(1,100)

def encrypt(plaintext, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(plaintext, AES.block_size))
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    return ct, iv

def decrypt(ciphertext, iv, key):
    try:
        iv = base64.b64decode(iv)
        ct = base64.b64decode(ciphertext)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt
    except (ValueError, KeyError):
        print('Incorrect decryption')

def main():
    g = 5
    p = 37
    print(f'g = {g}')
    print(f'p = {p}')

    a = generate_random_number()
    print(f"Alice's secret number: a = {a}")
    b = generate_random_number()
    print(f"Bob's secret number: b = {b}")

    print('Key exchanging...')
    s = key_exchange(p,g,a,b)
    print(f'The common computed value: s = {s}')
    hash = hashlib.md5(str(s).encode('utf-8'))
    s = hash.hexdigest()
    print(f'Hash of s: {s}')

    plaintext = b'Hello'
    print(f'Plaintext: {plaintext}')
    print('Encrypting...')
    ciphertext, iv = encrypt(plaintext, s.encode())
    print(f'Ciphertext: {ciphertext}')
    print('Decrypting...')
    decrypted_text = decrypt(ciphertext, iv, s.encode())
    print(f'Decrypted text: {decrypted_text}')

if __name__ == '__main__':
    main()