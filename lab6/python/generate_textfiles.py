# generate 25 text files with randomly chosen words inside
import random

DICT_FILE = 'english_dictionary.txt'
OUTPUT_PATH = './txts/'
NUM_OF_OUTPUT_FILES = 25

dictionary = []

with open(DICT_FILE, 'r') as dict_file:
    dictionary = dict_file.readlines()

n = len(dictionary)
for f in range(NUM_OF_OUTPUT_FILES):
    size = random.randint(100,500)
    content = []
    
    for s in range(size):
        word = dictionary[random.randint(0,n-1)]
        content.append(word)
    
    with open(f'{OUTPUT_PATH}{f+1}.txt', 'w') as fp:
        fp.write(''.join(content))