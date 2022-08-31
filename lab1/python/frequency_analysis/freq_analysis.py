import string, sys

FREQ_TABLE = englishLetterFreq = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 
    'O': 7.51, 'I': 6.97, 'N': 6.75, 
    'S': 6.33, 'H': 6.09, 'R': 5.99, 
    'D': 4.25, 'L': 4.03, 'C': 2.78, 
    'U': 2.76, 'M': 2.41, 'W': 2.36, 
    'F': 2.23, 'G': 2.02, 'Y': 1.97, 
    'P': 1.93, 'B': 1.29, 'V': 0.98, 
    'K': 0.77, 'J': 0.15, 'X': 0.15, 
    'Q': 0.10, 'Z': 0.07
}
ALPHABET = string.ascii_uppercase
ETAOIN = 'etaoinshrdlcumwfgypbvkjxqz'.upper()

def count_letter(text):
    letter_count = {}
    for letter in ALPHABET:
        letter_count[letter] = 0

    for letter in text:
        if letter in letter_count:
            letter_count[letter] += 1

    n = len(text)
    for letter in letter_count:
        letter_count[letter] /= n
    return letter_count

def extract_most_freq(count_dict):
    # sorting by descending order
    ordered_letter_count = list(sorted(count_dict.items(), 
                                key=lambda x:x[1],reverse=True))
    
    # return the substitution string like ETAOIN
    return ''.join([tup[0] for tup in ordered_letter_count])

def decryption(ciphertext):
    substitution = extract_most_freq(count_letter(ciphertext))

    # sorted_substitution = ''.join(sorted(substitution))
    # sorted_etao = ''.join([ ETAOIN[substitution.find(letter)] for letter in sorted_substitution])
    print(f'{substitution}: naive substitution string')
    print(f'{ETAOIN}: ETAOIN string')
    

    plaintext = []
    for letter in ciphertext:
        index = substitution.find(letter)
        if index == -1:
            plaintext.append(letter)
            continue

        plaintext.append(ETAOIN[index])
    return ''.join(plaintext)

def main():
    with open(sys.argv[1], 'r') as text_file:
        ciphertext = text_file.read()
    
    print(f'Plaintext:\n{decryption(ciphertext)}')

if __name__ == '__main__':
    main()



