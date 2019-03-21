import nltk

t = "i I you she he her they their"
token = nltk.word_tokenize(t)
tags = nltk.pos_tag(token)
print(tags)

