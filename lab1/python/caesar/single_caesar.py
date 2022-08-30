from caesar_cipher import decryption
import time, sys

def main():
    text = 'SEHH PWGA PDA NEJC PK IKNZKN, PDKQCD E ZK JKP GJKS PDA SWU'
    
    key = int(sys.argv[1])
    start = time.time()
    result = decryption(text, key)
    end = time.time()

    print(f'{result}')
    print(f'Execution time: {end - start}')

if __name__ == '__main__':
    main()