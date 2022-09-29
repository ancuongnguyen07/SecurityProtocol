from fileinput import filename
import sqlite3
import glob
import sys
import hashlib
import time
sys.path.insert(0, '../../lab2/python/Symmetric_Cipher')
import symmetric_cipher as sc

INPUT_PATH = './txts/'
SECRET_KEY = sc.generate_key()
IV_LIST = {} # IVs used for encrypting/decrypting files
IV_DICT = {} # IVs used for encrypting/decrypting keyvalues

DB_FILE = 'sse.db'
SQL_CONN = sqlite3.connect(DB_FILE)
DB_CUR = SQL_CONN.cursor()


def list_files(path):
    return glob.glob(f'{path}*.txt', recursive=True)

def generate_hash(plaintext):
    h = hashlib.new('sha256')
    h.update(plaintext.encode('utf-8'))
    return h.hexdigest()

def hash_keyword(keyword):
    return generate_hash(keyword)

def compute_keywords_key(hashed_keyword, keywords_numsearch):
    # K = SHA256(hashed_keyword + numsearch)
    return generate_hash(hashed_keyword + str(keywords_numsearch))

def compute_keywords_address(keywords_key, keywords_numfiles):
    # address = SHA256(keywords_key + numfiles)
    return generate_hash(keywords_key + str(keywords_numfiles))

def compute_keyvalue(filename, keywords_numfile, secret_key):
    # keyvalue = E_secret_key(filename + numfiles)
    plaintext = filename + str(keywords_numfile)
    iv, ciphertext = sc.encrypt(plaintext, secret_key)
    IV_DICT[plaintext] = iv
    return ciphertext

def encrypt_file(file_name, file_content):
    iv, ciphertext = sc.encrypt(file_content, SECRET_KEY)
    IV_LIST[file_name] = iv
    return ciphertext

def decrypt_file(file_name, file_content):
    return sc.decrypt(IV_LIST[file_name], file_content, SECRET_KEY)

def save_encrypted_file(file_name, ciphertext):
    file_path = f'{INPUT_PATH}{file_name}'
    with open(file_path, 'w') as fp:
        fp.write(ciphertext)
    return file_path

def keyword_processing(file_name, keyword, numfiles, numsearch):
    hashed_keyword = hash_keyword(keyword)
    keyword_key = compute_keywords_key(hashed_keyword, numsearch)
    keyword_address = compute_keywords_address(keyword_key, numfiles)
    keyvalue = compute_keyvalue(file_name, numfiles, SECRET_KEY)
    return hashed_keyword, keyword_address, keyvalue

def insert_processed_kw_db(id, hashed_keyword, keyword_address,
                        keyvalue, numsearch, numfiles):

    DB_CUR.execute('INSERT INTO sse_keywords VALUES(?,?,?,?)', (id, hashed_keyword,
                                                    numfiles, numsearch))
    SQL_CONN.commit()

    DB_CUR.execute('INSERT INTO sse_csp_keywords VALUES(?,?,?)', (id, keyword_address, keyvalue))
    SQL_CONN.commit()

def update_numfile_kw_db(id, numfiles):
    DB_CUR.execute("""UPDATE sse_keywords
    SET sse_keyword_numfiles = :numfile WHERE sse_keywords_id = :id
    """, {'numfile': numfiles,'id': id})
    SQL_CONN.commit()

def create_dictionary(path):
    text_file_list = list_files(path)
    keyword_dict = {}

    id_counter = 0
    for file_path in text_file_list:
        file_name = file_path.split('/')[-1]
        # print(f'Processing: {file_name}...')
        with open(file_path, 'r') as txt_file:
            file_content = txt_file.read().strip()

        keywords_list = file_content.split('\n')
        for keyword in keywords_list:
            if keyword in keyword_dict:
                keyword_dict[keyword] += 1
            else:
                keyword_dict[keyword] = 1
                id_counter += 1
            numfiles = keyword_dict[keyword]

            hashed_keyword, keyword_address, keyvalue = keyword_processing(file_name,
                                                        keyword,numfiles,0)
            
            # save to database
            if numfiles == 1:
                insert_processed_kw_db(id_counter,hashed_keyword, keyword_address, keyvalue,
                                            0, numfiles)
            else:
                update_numfile_kw_db(id_counter, numfiles)

        # encrypt text file
        file_name = file_path.split('/')[-1]
        ciphertext = encrypt_file(file_name,file_content)
        save_encrypted_file(file_name, ciphertext)
        
        # check if the encryption/decrytion went well
        # with open(encrypted_file_path, 'r') as fp:
        #     content = fp.read()
        # decrypted_text = decrypt_file(file_name, content)
        # assert file_content == decrypted_text
        
def search_keyword(keyword):
    pass

def main():
    # sql_conn = sqlite3.connect(DB_FILE) # connect to the DB file
    # db_cur = sql_conn.cursor()
    
    print('Creating a dictionary and encrypting plaintext files...')
    start = time.time()
    create_dictionary(INPUT_PATH)
    end = time.time()
    print(f'Execution time of creating dictionary and encrypting .txt files: {end-start}')


if __name__ == '__main__':
    main()