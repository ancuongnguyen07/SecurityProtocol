from collections import Counter
import string

ALPHABET = string.ascii_uppercase

# def bin_to_char(bin_str):
#     index = int(bin_str, 2)
#     return ALPHABET[ index % 26]

def ngrams (text, n=3):
    return zip(*[text[i:] for i in range(n)])

CIPHER_BLOCKS = [
    '010001', '001100', '110000', '000101', '010110', '110000', '011010', '110000', '000111', '100011',
    '011010', '110000', '000110', '001010', '111000', '010110', '000110', '110000', '010101', '000110',
    '010010', '010110', '111000', '010011', '011100', '000101', '010011', '010100', '101000', '110000',
    '000110', '001010', '100011', '011010', '010100', '100011', '010010', '100100', '111000', '010011',
    '011010', '000101', '011010', '110000', '101010', '010010', '000101', '000110', '110000', '010100',
    '100011', '010010', '011000', '111000', '001100', '001100', '100100', '111000', '011100', '010010',
    '101001', '110000', '100011', '010010', '000110', '000110', '001010', '000101', '000110', '000110',
    '001010', '110000', '000110', '110000', '010101', '000110', '011000', '000101', '010110', '110000',
    '010011', '000111', '101001', '010100', '010001', '000110', '110000', '011010', '010010', '010110',
    '111000', '010011', '011100', '000110', '001010', '110000', '010110', '010010', '001001', '010110',
    '000110', '111000', '000110', '010010', '000110', '111000', '100011', '010011', '000111', '111000',
    '010001', '001010', '110000', '101001', '000101', '100100', '000110', '110000', '101001', '010100',
    '100011', '010010', '100100', '100011', '010010', '010011', '011010', '000101', '010110', '100011',
    '001100', '010010', '000110', '111000', '100011', '010011', '010001', '001100', '110000', '000101',
    '010110', '110000', '011010', '110000', '010110', '000111', '101001', '111000', '001001', '110000',
    '001010', '100011', '011000', '010100', '100011', '010010', '000101', '010011', '000101', '001100',
    '010100', '001011', '110000', '011010', '000110', '001010', '110000', '000110', '110000', '010101',
    '000110', '001010', '111000', '010011', '000110', '010100', '100011', '010010', '101000', '000101',
    '010100', '010010', '010110', '110000', '000101', '010011', '010100', '010001', '101001', '100011',
    '011100', '101001', '000101', '101000', '100011', '101001', '010110', '111000', '101000', '010001',
    '001100', '010100', '000111', '100011', '010010', '010011', '000110', '000110', '001010', '110000',
    '100100', '101001', '110000', '101010', '010010', '110000', '010011', '000111', '111000', '110000',
    '010110', '100011', '100100', '000101', '001100', '001100', '000110', '001010', '110000', '010001',
    '111000', '000111', '000110', '010010', '101001', '110000', '010110', '000110', '001010', '000101',
    '000110', '000101', '010001', '010001', '110000', '000101', '101001', '011000', '111000', '000110',
    '001010', '111000', '010011', '000110', '001010', '110000', '000110', '110000', '010101', '000110',
    '001010', '000101', '110100', '110000', '100100', '010010', '010011'
]

replacement = {'110000': 'E', '000110':'T', '001010': 'H','000101': 'A','010101':'X'}
plaintext = ''.join(replacement[block] if block in replacement else '*' for block in CIPHER_BLOCKS)

counts = Counter(ngrams(CIPHER_BLOCKS))

print(counts.most_common(5))
# plaintext = ''.join([bin_to_char(block) for block in CIPHER_BLOCKS])
# print(plaintext)