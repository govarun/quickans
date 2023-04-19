import PyPDF2
from tika import parser
import random
from gensim.parsing.preprocessing import remove_stopwords
import numpy as np
import string

pdf = parser.from_file('/home/ishikaa2/quickans/ans_generator/data/ir_txt/410_textbook.pdf')
data = pdf['content']

f = open('textbook_text', 'w')
f.write(data)
f.close()
