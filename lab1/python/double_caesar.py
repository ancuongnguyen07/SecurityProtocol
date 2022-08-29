from caesar_cipher import decryption
import time

def double_decryption(ciphertext, key1, key2):
    return decryption(decryption(ciphertext, key1), key2)

def main():
    ciphertext = 'SEHH PWGA PDA NEJC PK IKNZKN, PDKQCD E ZK JKP GJKS PDA SWU'
    key1 = 13
    key2 = 9

    start = time.time()
    print(double_decryption(ciphertext, key1, key2))
    end = time.time()
    print(f'Execution time: {end - start}')

if __name__ == "__main__":
    main()