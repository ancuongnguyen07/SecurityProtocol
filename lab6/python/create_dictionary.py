import sqlite3
import glob
import sys
sys.path.insert(0, '../../lab2/python/Symmetric_Cipher')
import symmetric_cipher as sc

INPUT_PATH = './txts/'
SECRET_KEY = sc.generate_key()

def list_files(path):
    return glob.glob(f'{path}*.txt', recursive=True)

def extract_keywords(path):
    file_list = list_files(path)
    keywords = []
    for file_name in file_list:
        with open(file_name, 'r')  as fp:
            keywords.extend(fp.readlines())
    return list(map(lambda x:x.rstrip('\n'), keywords))

def encrypt_files(plaintext_list, secret_key):
    iv_list = []
    ciphertext_list = []
    for plaintext in plaintext_list:
        iv, ciphertext = sc.encrypt(plaintext, secret_key)
        iv_list.append(iv)
        ciphertext_list.append(ciphertext)
    return iv_list, ciphertext_list

def decrypt_files(iv_list, ciphertext_list, secret_key):
    plaintext_list = []
    assert len(iv_list) == len(ciphertext_list)
    for i in range(len(iv_list)):
        plaintext = sc.decrypt(iv_list[i],ciphertext_list[i],secret_key)
        plaintext_list.append(plaintext)
    return plaintext_list

def extract_plaintext(path):
    file_list = list_files(path)
    plaintext_list = []
    for file_name in file_list:
        with open(file_name, 'r')  as fp:
            content = ''.join(fp.readlines())
            plaintext_list.append(content)
    return plaintext_list

def main():
    plain_keywords = extract_keywords(INPUT_PATH)

    # encrypt text files using AES
    plaintext_list = extract_plaintext(INPUT_PATH)
    iv_list, ciphertext_list = encrypt_files(plaintext_list, SECRET_KEY)
    # save encrypted files
    # for i in range(len(ciphertext_list)):
    #     with open(f'{INPUT_PATH}encrypted/{i+1}.txt', 'w') as fp:
    #         fp.write(ciphertext_list[i])

    # decrypt text files
    decryptedtext_list = decrypt_files(iv_list, ciphertext_list, SECRET_KEY)
    # check if the encryption/decryption process went well
    for i in range(len(decryptedtext_list)):
        assert decryptedtext_list[i] == plaintext_list[i]

if __name__ == '__main__':
    main()