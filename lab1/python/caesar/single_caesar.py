from caesar_cipher import decryption
import time, sys

def main():
    text = 'SEHH PWGA PDA NEJC PK IKNZKN, PDKQCD E ZK JKP GJKS PDA SWU'
    start = time.time()
    key = int(sys.argv[1])
    result = decryption(text, key)
    end = time.time()

    print(f'{result}')
    print(f'Execution time: {end - start}')

if __name__ == '__main__':
    main()