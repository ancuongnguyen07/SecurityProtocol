import sys
from Crypto.PublicKey import ECC

def generate_key_pairs(id):
    private_key = ECC.generate(curve='P-256')
    public_key = private_key.public_key()

    with open(f'{id}_key.pub', 'w') as f:
        f.write(public_key.export_key(format='PEM'))
    with open(f'{id}_key.pri', 'w') as f:
        f.write(private_key.export_key(format='PEM'))

def main():
    generate_key_pairs(sys.argv[1])

if __name__ == '__main__':
    main()