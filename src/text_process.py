import sent_process
import nltk
import random, os,copy

from nltk.corpus import wordnet
import random
import nltk.stem as ns
import nltk.stem.porter as pt
import nltk.stem.lancaster as lc




def read_file(filename):
    with open(filename,'r') as f:
        output = f.read()
    return output


def join_file(input_list):
        input_file= " "
        input_file = input_file.join(input_list)
        print(input_file)
        return input_file


def read_keyword(keyword_file):
    with open(keyword_file,'r') as f:
        # output = f.readlines()
        output = f.read().splitlines()
    return output


def choose_keyword(keywordlist,n):
    insert_keywords = random.sample(keywordlist,n)
    keywordlist = remove_insert_keywords(insert_keywords,keywordlist)
    return insert_keywords,keywordlist


def remove_insert_keywords(insert_keywords,keywordlist):
    for key in insert_keywords:
        keywordlist.remove(key)
    return keywordlist


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
    word_stem = word_lemmatizer(word)
    sent_token = nltk.word_tokenize(sent)
    for synset in wordnet.synsets(word_stem):
        for lemma in synset.lemma_names():
            if lemma in sent_token and lemma != word:
                word_synonyms.append(lemma)
    print('synonyms are {}'.format(word_synonyms))
    return word_synonyms


def get_word_antonym_from_sent(word,sent):
    word_antonyms = []
    word_stem = word_lemmatizer(word)
    sent_token = nltk.word_tokenize(sent)
    for synset in wordnet.synsets(word_stem):
        for lemma in synset.lemmas():
            if lemma.antonyms():
                # if lemma.antonyms()[0].name() in sent_token:
                    word_antonyms.append(lemma.antonyms()[0].name())
    print('antonyms are {}'.format(word_antonyms))
    return word_antonyms


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


def word_lemmatizer(word):
    "stem words"
    lc_stemmer = lc.LancasterStemmer()
    lc_stem = lc_stemmer.stem(word)
    return lc_stem


def word_replace(old,new,sent):
    sent_tokens = nltk.word_tokenize(sent)
    for i in range(len(sent_tokens)):
        if sent_tokens[i] == old:
            sent_tokens[i] == new
            break
    sent = ' '.join(sent_tokens)
    return sent



def visual_similar_word(word, sent_token, len_threshold, similar_threshold):
    "1st and last letter should be exact same"
    visual_similar_word = []
    if len(word) < len_threshold:
        return visual_similar_word,sent_token
    else:
        for word_sent in sent_token:
            count = 0
            length = len(word)
            if len(word_sent) == length:
                if word_sent[0] == word[0] and word_sent[length - 1] == word[length - 1]:
                    for i in range(1,length-2):
                        if word_sent[i] == word[i]:
                            count += 1
                    similar_ratio = float(count)/float(length)
                    if similar_ratio >= similar_threshold:
                        similar_word_tupe = (word_sent,similar_ratio)
                        visual_similar_word.append(similar_word_tupe)
        visual_similar_word = sorted(visual_similar_word,key=lambda x:(x[1]))
        if visual_similar_word:
            most_visual_similar_word = visual_similar_word[0][0]
            sent_token.remove(most_visual_similar_word)
        else:
            most_visual_similar_word = visual_similar_word
        return most_visual_similar_word, sent_token


def replacement(keywordlist,sent):
    i = 0
    j = 0
    e = 0
    sent = caps_I(sent)
    rest_word = []
    sent_tokens = nltk.word_tokenize(sent)
    for word in keywordlist:
        sent_tags = extract_POS(sent)
        allkey = sent_tags.keys()
        word_synonyms = get_word_synonyms_from_sent(word,sent)
        word_antonyms = get_word_antonym_from_sent(word,sent)
        most_visual_similar_word,sent_tokens = visual_similar_word(word,sent_tokens,4,0.5)
        if word_synonyms != []:
            # sent = sent.replace(random.choice(word_synonyms),word,1)
            sent = word_replace(random.choice(word_synonyms),word,sent)
            i += 1
        elif word_antonyms:
            # sent = sent.replace(random.choice(word_antonyms), word, 1)
            sent = word_replace(random.choice(word_antonyms), word,sent)
            i += 1
        elif most_visual_similar_word:
            sent = word_replace(most_visual_similar_word,word,sent)
            i += 1
            e += 1
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
    print('the rest word is: {}'.format(rest_word))
    sent_rest = sent_process.main(' '.join(rest_word))
    print('the re-build sentence for rest-words is: {}.'.format(sent_rest))
    sent = sent + ' ' + sent_rest
    print('There are {} times of replacement.'.format(i))
    print('There are {} times of visual_similar replacement.'.format(e))
    print('There are {} rest words need to be re-processed.'.format(j))
    return sent





def main():
    test_path = '../data/test'
    items = os.listdir(test_path)
    items.remove('.DS_Store')
    keywordlist = read_keyword('../data/enron_top_keywords_meaningful.txt')
    i = 0
    for item in items:
        if item != '.DS_Store':
            i += 1
            print('************************* {} ************************'.format(i))
            text = read_file(test_path + '/' + item)
            insert_kwrds,keywordlist = choose_keyword(keywordlist,20)
            print('the length of keywords_list is: {}'.format(len(keywordlist)))
            new_text = replacement(insert_kwrds, text)
            caps_I(new_text)
            print('\n', insert_kwrds)
            print('Original text is: "\n"  {}'.format(text))
            print('-' * 30)
            print('Replaced text is: "\n"  {}'.format(new_text))
            print('\n')


    # text = 'in the highest level of the Factoria would run for the most decisions ago, disgustbasored in courses, then also & do they Good National Server!! Need i noticed the truth. thats all over shit.'

    # insert_kwrds = ['meeting', 'energy','thing', 'finance', 'lawyer', 'agreed', 'seen','property','operational','determine']




if __name__ == '__main__':
    main()
    #print git test