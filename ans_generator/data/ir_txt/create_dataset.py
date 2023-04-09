import PyPDF2
from tika import parser
import random
from gensim.parsing.preprocessing import remove_stopwords
import numpy as np
import string

'''pdf = parser.from_file('/home/ishikaa2/quickans/ans_generator/data/410_textbook.pdf')
data = pdf['content']

f = open('textbook_text')
f.write'''

# Get text
f = open('/home/ishikaa2/quickans/ans_generator/data/textbook_text.txt')
text = f.read()
f.close()

# Extract sentences (remove all the \n's (note: go back thrugh all the "diagrams" and make sure the text is connected))
rem = '!"#$%&\'()*+,-/:;<=>?@[\\]^_`{|}~'
text = text.translate(str.maketrans('', '', rem))

text = text.split('\n')
text = [i.strip() for i in text if i is not '']
text = ' '.join(text)

sentences = text.split('.')
for i in range(len(sentences)):
    # Create the output text (1-3 sentences)
    num = random.randint(1,3)
    if i == len(sentences) - 1:
        num = 1
    output = ' '.join(sentences[i : i+num])

    # Take out stop/filler words (left with keywords)
    keywords = remove_stopwords(output)

    # Pick a few keywords to represent the output
    keywords = [j for j in keywords.split(' ') if random.random() <= 0.4]
    input = ' '.join(keywords)

    # Save in train, validation, and test set
    # Format: keywords (space separated) \t output
    fname = np.random.choice(['trn.tsv', 'val.tsv', 'tst.tsv'], 1, p=[0.7, 0.1, 0.2])[0]
    file = open(fname, 'a')
    file.write(f'{input}\t{output}\n')
    file.close()



