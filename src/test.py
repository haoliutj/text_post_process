import nltk

t = 'I laywer'
token = nltk.word_tokenize(t)
tags = nltk.pos_tag(token)
print(tags)
