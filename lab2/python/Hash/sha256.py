from Crypto.Hash import SHA256
import sys

# insprired by https://pycryptodome.readthedocs.io/en/latest/src/hash/sha256.html

def compute_hash(file):
    hash_object = SHA256.new(open(file, 'rb').read())
    return hash_object.hexdigest()

def verify_hash(file, given_hash):
    hash = compute_hash(file)
    return hash == given_hash

def main():
    mode = sys.argv[1]
    if mode == '-c':
        file_path = sys.argv[2]
        print(compute_hash(file_path))
    elif mode == '-v':
        file_path, hash = sys.argv[2:4]
        print(hash == compute_hash(file_path))
    else:
        print(f'Invalid option')
        return

if __name__ == '__main__':
    main()
