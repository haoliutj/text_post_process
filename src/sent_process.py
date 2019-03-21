import nltk


token = ['test']

def raise_error(exception):
    pass


def gen_POS(token):
    tags = nltk.pos_tag(token)
    return tags


def parse_interjection(dic):
    """
    extract words POS_UH like "wow..."
    :param dic:
    :return:
    """
    uh = dic['UH']
    if uh:
        return uh
    else:
        raise_error('UH list is empty.')


def parse_determiner(dic):
    """
    extract words like 'the, a ,no'
    :param dic:
    :return:
    """
    tag_dt = ['DT','PDT']
    dts = []
    for key in tag_dt:
        dts += dic[key]
    if dts:
        return dts
    else:
        raise_error('Determiner list is empty.')


def parse_adjective(dic):
    tag_jj = ['JJ','JJS','JJR']
    jj = []
    for key in tag_jj:
        jj += dic[key]
    if jj:
        return jj
    else:
        raise_error('Adjective list is empty.')



def parse_subject(dic):
    tag_sub = ['NN','NNS','NNP','NNPS']
    subs = []
    for key in tag_sub:
        subs += dic[key]
    if subs:
        return subs
    else:
        raise_error('Subject list is empty.')


def parse_predicate(dic):
    tag_pred = ['VB','VBD','VBG','VBN','VBP','VBZ']
    pred = []
    for key in tag_pred:
        pred += dic[key]
    if pred:
        return pred
    else:
        raise_error('Predicate list is empty')

def parse_conjunction(dic):
    tag_conj = ['RP','TO','IN','WDT','WP']
    conj = []
    for key in tag_conj:
        conj += dic[key]
    if conj:
        return conj
    else:
        raise_error('Conjunctin list is empty.')


def parse_object(subjects):
    """
    share with parse_subject
    :param subjects:
    :return:
    """
    objs = subjects
    if objs:
        return objs
    else:
        raise_error('Object list is empty.')


def parse_comma(dic):
    marks = []
    marks = dic['.']
    if marks:
        return marks
    else:
        raise_error('Marks list is empty.')


