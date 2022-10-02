import sqlite3
import glob
import sys
import hashlib
import time
import base64
sys.path.insert(0, '../../lab2/python/Symmetric_Cipher')
import symmetric_cipher as sc

INPUT_PATH = './txts/'
SECRET_KEY = sc.generate_key()
IV_FILE_CRYPTO = {} # IVs used for encrypting/decrypting files
IV_KEYVALUE = {} # IVs used for encrypting/decrypting keyvalues

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
    str_numfile = str(keywords_numfile)
    plaintext = f'{filename},{str_numfile}'
    iv, ciphertext = sc.encrypt(plaintext, secret_key)
    IV_KEYVALUE[ciphertext] = iv
    return ciphertext

def encrypt_file(file_name, file_content):
    iv, ciphertext = sc.encrypt(file_content, SECRET_KEY)
    IV_FILE_CRYPTO[file_name] = iv
    # decrypted_text = sc.decrypt(iv, ciphertext, SECRET_KEY)
    # assert decrypted_text == file_content, 'decrypted ciphertext does not match plaintext'
    return ciphertext

def decrypt_file(file_name, file_content):
    return sc.decrypt(IV_FILE_CRYPTO[file_name], file_content, SECRET_KEY)

def save_encrypted_file(file_name, ciphertext):
    file_path = f'{file_name}'
    with open(file_path, 'w') as fp:
        fp.write(ciphertext)
    return file_path

def keyword_processing(file_name, keyword, numfiles, numsearch):
    hashed_keyword = hash_keyword(keyword)
    keyword_key = compute_keywords_key(hashed_keyword, numsearch)
    keyword_address = compute_keywords_address(keyword_key, numfiles)
    keyvalue = compute_keyvalue(file_name, numfiles, SECRET_KEY)
    return hashed_keyword, keyword_address, keyvalue

def insert_processed_kw_db(hashed_keyword, keyword_address,
                        keyvalue, numsearch, numfiles):

    DB_CUR.execute('INSERT INTO sse_keywords VALUES(?,?,?,?)', (None, hashed_keyword,
                                                    numfiles, numsearch))
    SQL_CONN.commit()

    DB_CUR.execute('INSERT INTO sse_csp_keywords VALUES(?,?,?)', (None, keyword_address, keyvalue))
    SQL_CONN.commit()

def update_numfile_kw_db(hashed_keyword, numfiles):
    DB_CUR.execute("""UPDATE sse_keywords
    SET sse_keyword_numfiles = :numfile WHERE sse_keyword = :hash
    """, {'numfile': numfiles,'hash': hashed_keyword})
    SQL_CONN.commit()

def create_dictionary(path):
    text_file_list = list_files(path)
    keyword_dict = {}

    start = time.time()

    for file_path in text_file_list:
        file_name = file_path.split('/')[-1]
        # print(f'Processing: {file_name}...')
        with open(file_path, 'r') as txt_file:
            file_content = txt_file.read().strip()

        keywords_list = file_content.split('\n')
        for keyword in keywords_list:
            if keyword not in keyword_dict:
                keyword_dict[keyword] = []
            keyword_dict[keyword].append(file_name)


    for keyword in keyword_dict:
        numfiles = len(keyword_dict[keyword])

        hashed_keyword, keyword_address, keyvalue = keyword_processing(
                                                ','.join(keyword_dict[keyword]),
                                                    keyword,numfiles,0)
        # save to database
        insert_processed_kw_db(hashed_keyword, keyword_address, keyvalue,
                                        0, numfiles)

    # encrypt text file
    for file_path in text_file_list:
        file_name = file_path.split('/')[-1]
        file_content = open(file_path, 'r').read().strip()
        ciphertext = encrypt_file(file_name, file_content)
        save_encrypted_file(f'{INPUT_PATH}encrypt/{file_name}', ciphertext)

    end = time.time()
    print(f'Execution time of creating dictionary and encrypting .txt files: {end-start}')

    # save secret key and IVs
    with open('key.priv', 'wb') as fp:
        fp.write(base64.b64encode(SECRET_KEY))

    with open('iv_file.priv', 'wb') as fp:
        for key in IV_FILE_CRYPTO:
            content = base64.b64encode(IV_FILE_CRYPTO[key])
            fp.write(key.encode())
            fp.write(b',')
            fp.write(content)
            fp.write(b'\n')
            
    with open('iv_keyvalue.priv', 'wb') as fp:
        for key in IV_KEYVALUE:
            content = base64.b64encode(IV_KEYVALUE[key])
            fp.write(key.encode())
            fp.write(b',')
            fp.write(content)
            fp.write(b'\n')

    iv_file = retrieve_iv_file('iv_file.priv')

    key = retrieve_secret_key()
    assert key == SECRET_KEY, 'priv_keys do not match'

    for file_name in IV_FILE_CRYPTO:
        assert IV_FILE_CRYPTO[file_name] == iv_file[file_name], f'{file_name} IV: does not match'
    
    for file_path in text_file_list:
        file_name = file_path.split('/')[-1]
        file_content = open(file_path, 'r').read().strip()
        ciphertext = open(f'{INPUT_PATH}encrypt/{file_name}', 'r').read()
        decrypted_text = sc.decrypt(iv_file[file_name], ciphertext, key)
        assert decrypted_text == file_content
    
    # check if the encryption/decrytion went well
    # with open(encrypted_file_path, 'r') as fp:
    #     content = fp.read()
    # decrypted_text = decrypt_file(file_name, content)
    # assert file_content == decrypted_text

def check_retrieve_IV_correctly():
    iv_file = retrieve_iv_file('iv_file.priv')

    key = retrieve_secret_key()

    ciphertext = open('txts/encrypt/1.txt', 'r').read()

    decrypted_text = sc.decrypt(iv_file['1.txt'], ciphertext, key)
    with open('temp.txt', 'w') as fp:
        fp.write(decrypted_text)
    plaintext = open('txts/1.txt', 'r').read().strip()

    assert plaintext == decrypted_text, 'the plaintext file and the decrypted file does not match'

def retrieve_iv_file(file_path):
    ivs = {}
    with open(file_path, 'rb') as fp:
        for line in fp:
            file_name, iv = line.split(b',')
            ivs[file_name.decode()] = base64.b64decode(iv)
    return ivs

def update_numsearch_kw_db(hashed_keyword, numsearch):
    DB_CUR.execute("""UPDATE sse_keywords
    SET sse_keyword_numsearch = :numsearch WHERE sse_keyword = :hash
    """, {'numsearch': numsearch,'hash': hashed_keyword})
    SQL_CONN.commit()

def update_keywords_address_kw_db(id, new_keyword_address):
    DB_CUR.execute('''UPDATE sse_csp_keywords
    SET csp_keywords_address = :address WHERE csp_keywords_id = :id
    ''', {'id': id, 'address': new_keyword_address})
    SQL_CONN.commit()

def search_numfile_numsearch(hashed_keyword):
    res = DB_CUR.execute('''SELECT sse_keywords_id,sse_keyword_numfiles,sse_keyword_numsearch
    FROM sse_keywords WHERE sse_keyword = :keyword''', {'keyword':hashed_keyword})

    entries = res.fetchall()
    assert len(entries) == 1, 'duplicated hash value or empty return!!!!'
    id, numfile, numsearch = entries[0]
    return id, numfile, numsearch

def recompute_parameters(id, hashed_keyword, numsearch, numfile):
    numsearch += 1
    keyword_key = compute_keywords_key(hashed_keyword, numsearch)
    keyword_address = compute_keywords_address(keyword_key, numfile)
    update_keywords_address_kw_db(id, keyword_address)
    update_numsearch_kw_db(hashed_keyword, numsearch)

def retrieve_keyvalue(keyword_address):
    res = DB_CUR.execute(''' SELECT csp_keyvalue
    FROM sse_csp_keywords WHERE csp_keywords_address = :address
    ''', {'address': keyword_address})

    entries = res.fetchall()
    assert len(entries) == 1, 'duplicated IDs or empty return!!!'
    return entries[0][0]

def retrieve_secret_key():
    priv_key = None
    with open('key.priv', 'rb') as fp:
        priv_key = fp.read()
    return base64.b64decode(priv_key)

def search_keyword(keyword, iv_file, iv_keyvalue, secret_key):
    start = time.time()

    print(f'Searching "{keyword}"...')
    hashed_keyword = hash_keyword(keyword)
    id, numfile, numsearch = search_numfile_numsearch(hashed_keyword)
    keyword_key = compute_keywords_key(hashed_keyword, numsearch)
    keyword_address = compute_keywords_address(keyword_key,numfile)
    keyvalue = retrieve_keyvalue(keyword_address)
    file_name_numfile = sc.decrypt(iv_keyvalue[keyvalue],
                        keyvalue,secret_key)

    file_list = list(file_name_numfile.split(',')[:-1])
    end = time.time()

    print("Files containing '%s': %s" % (keyword,','.join(file_list)))
    print(f'Searching time: {end - start}')

    print('Decrypting files...')
    start = time.time()
    for file_name in file_list:
        with open(f'{INPUT_PATH}encrypt/{file_name}', 'r') as fp:
            content = fp.read()
        decrypted_text = sc.decrypt(iv_file[file_name],content,secret_key)
        with open(f'{INPUT_PATH}decrypt/{file_name}', 'w') as fp:
            fp.write(decrypted_text)
    end = time.time()
    print('All decrypted files were moved into the "decrypt" folder')
    print(f'Decrypting time: {end - start}')
    
    recompute_parameters(id, hashed_keyword, numsearch, numfile)

def main():
    assert len(sys.argv) == 2, 'You should choose mode -i,-s and no other arguments'
    mode = sys.argv[1]
    assert mode == '-i' or mode == '-s'

    if mode == '-i':
        # print('Creating a dictionary and encrypting plaintext files...')
        create_dictionary(INPUT_PATH)
    else:
        # searching function
        secret_key = retrieve_secret_key()
        iv_file_crypt = retrieve_iv_file('iv_file.priv')
        iv_keyvalue = retrieve_iv_file('iv_keyvalue.priv')
        keyword = input('Which word do you want to find? ')
        search_keyword(keyword,iv_file_crypt,iv_keyvalue,secret_key)

    SQL_CONN.close()

if __name__ == '__main__':
    main()