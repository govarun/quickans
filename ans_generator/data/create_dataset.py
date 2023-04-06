import PyPDF2
from tika import parser

'''pdf = parser.from_file('/home/ishikaa2/quickans/ans_generator/data/410_textbook.pdf')
data = pdf['content']

f = open('textbook_text')
f.write'''

# Get text

# Extract sentences (remove all the \n's (note: go back thrugh all the "diagrams" and make sure the text is connected))

# Take out stop/filler words (left with keywords)

# Pair up keywords and paragraph

# Save in train, validation and test set
'''
where to restart:
Let’s look at how this new model works for our example. We ask the following
question: which of these documents is most likely the imaginary relevant docu
ment in the user’s mind when the user formulates this query? We quantify this
probability as a conditional probability of observing this query if a particular doc
ument is in fact the imaginary relevant document in the user’s mind. We compute
all these query likelihood probabilities—that is, the likelihood of the query given
each document. Once we have these values, we can then rank these documents
'''