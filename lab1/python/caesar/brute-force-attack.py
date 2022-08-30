import caesar_cipher as cc
import time

def BF_attack(ciphertext):
    for key_shift in range(cc.KEY_SPACE):
        print(f'{key_shift}: {cc.decryption(ciphertext, key_shift)}')

def main():
    ciphertext = 'BT LXVYUNCNM. HXD JAN ANJMH OXA CQN BNLDARCH YAXCXLXUB LXDABN- JMVRW'
    start = time.time()
    BF_attack(ciphertext)
    end = time.time()
    print(f'Execution time: {end - start}')

if __name__ == '__main__':
    main()