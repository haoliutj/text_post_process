import nltk

t = "wowm, oh, I you she he her they their."
token = nltk.word_tokenize(t)
tags = nltk.pos_tag(token)
print(tags)

h = ['i']
if h:
    print('not empty')
else:
    print('empty')



