import nltk

y = 'you are teenager'
y_tokens = nltk.word_tokenize(y)
for i in range(len(y_tokens)):
    if y_tokens[i] == 'are':
        y_tokens[i] = 'and'
a = ' '.join(y_tokens)

ss = y.replace('are','and',1)

print(ss)
print(y_tokens)