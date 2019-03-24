import sent_process
import nltk

from nltk.corpus import wordnet
import random



def read_file(filename):
    with open(filename,'r') as f:
        input = f.read()
    return input

def join_file(input_list):
        input_file= " "
        input_file = input_file.join(input_list)
        print(input_file)
        return input_file


def extract_POS(input_file):
    token = nltk.word_tokenize(input_file)
    # token = ['I' if x == 'i' else x for x in token] #replace 'i' with "I'
    # print('%'*40)
    # print(token)
    tags = nltk.pos_tag(token)
    # print(tags)
    dic = {}
    for word,tag in tags:
        if tag not in dic:
            dic[tag] = []
        dic[tag].append(word)

    return dic


def get_word_synonyms_from_sent(word, sent):
    word_synonyms = []
    sent_token = nltk.word_tokenize(sent)
    for synset in wordnet.synsets(word):
        for lemma in synset.lemma_names():
            if lemma in sent_token and lemma != word:
                word_synonyms.append(lemma)
    return word_synonyms


def check_substitution_list(keywrdlist,candidates):
    # if candidates is a sub-set of keywrdlsit
    # then return True
    i = 0
    for x in candidates:
        if x in keywrdlist:
            i += 1
    if i == len(candidates):
        flag = True
    else:
        flag = False
    return flag


def caps_I(sent):
    # replace i to I.
    sent_token = nltk.word_tokenize(sent)
    for i in range(len(sent_token)):
        if sent_token[i] == 'i':
            sent_token[i] = 'I'
    sent = (' '.join(sent_token))
    return sent


def replacement(keywordlist,sent):
    i = 0
    j = 0
    sent = caps_I(sent)
    rest_word = []
    for word in keywordlist:
        sent_tags = extract_POS(sent)
        allkey = sent_tags.keys()
        word_synonyms = get_word_synonyms_from_sent(word,sent)
        if word_synonyms != []:
            sent = sent.replace(random.choice(word_synonyms),word,1)
            i += 1
        else:
            tmp = []
            tmp.append(word)
            tag = nltk.pos_tag(tmp)[0][1]
            # print(sent_tags.get(tag))
            if tag in allkey:
                # print('{} has POS relatives.'.format(word))
                # print('POS is {}.'.format(sent_tags[tag]))
                candidates = sent_tags[tag]
                if not check_substitution_list(keywordlist,candidates):
                    if candidates is not None:
                        substitute = random.choice(sent_tags[tag])
                        while substitute in keywordlist:
                            substitute = random.choice(sent_tags[tag])
                        sent = sent.replace(substitute,word,1)
                        i += 1
                else:
                    # sent = sent + ' ' + word
                    rest_word.append(word)
                    j += 1
            else:
                # sent = sent + ' ' + word
                rest_word.append(word)
                j += 1
    print(rest_word)
    sent_rest = sent_process.main(' '.join(rest_word))
    print(sent_rest)
    sent = sent + sent_rest
    print('There are {} times of replacement.'.format(i))
    print('There are {} rest words need to be re-processed.'.format(j))
    return sent



def main():
    # input_list = read_file('../data/enron_top_keywords_test.txt')
    # extract POS for rnn_text
    text = 'in the highest level of the Factoria would run for the most decisions ago, disgustbasored in courses, then also & do they Good National Server!! Need i noticed the truth. thats all over shit.'
    # text_tags = extract_POS(text)

    # extract POS for inserted keywords
    insert_kwrds = ['meeting', 'energy','thing', 'finance', 'lawyer', 'agreed', 'seen','property','operational','determine']
    new_text = replacement(insert_kwrds,text)
    print('Original text is:||  {}.'.format(text))
    print('-'*30)
    print('Replaced text is:||  {}.'.format(new_text))

    caps_I(new_text)



if __name__ == '__main__':
    main()
    #print git test