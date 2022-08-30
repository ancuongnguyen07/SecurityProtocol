from caesar_cipher import decryption
import time, sys

def double_decryption(ciphertext, key1, key2):
    return decryption(decryption(ciphertext, key1), key2)

def main():
    ciphertext = 'SEHH PWGA PDA NEJC PK IKNZKN, PDKQCD E ZK JKP GJKS PDA SWU'
    key1 = int(sys.argv[1])
    key2 = int(sys.argv[2])

    start = time.time()
    result = double_decryption(ciphertext, key1, key2)
    end = time.time()
    print(result)
    print(f'Execution time: {end - start}')

if __name__ == "__main__":
    main()