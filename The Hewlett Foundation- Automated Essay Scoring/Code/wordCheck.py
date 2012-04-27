import sys, os

import nltk
from nltk.corpus import brown
from nltk.corpus import reuters

from basic_parsing import sent_seg
from basic_parsing import word_tokenize

data_path = '/Users/sinn/Documents/Kaggle/The Hewlett Foundation- Automated Essay Scoring'

def makeLower(docs):
    '''make all words lower-case'''
    for i,d in enumerate(docs):
        d = [w.lower() for w in d]
        docs[i] = d
    return docs

def getRWFrac(docs, words):
    '''Calcs fraction of words in each doc occuring in the words set'''
    RWFracs = dict()
    for i,d in enumerate(docs):
        count = sum([(w in words)*1 for w in d])
        frac = float(count)/len(d)
        RWFracs[i] = frac
    return RWFracs
        
def makeWordSet(args=None):
    '''Use the Brown corpus to see how many words used'''
    word_set = set()
    for cat in brown.categories():
        word_set = word_set.union(set(brown.words(categories=cat)))
    for cat in reuters.categories():
        word_set = word_set.union(set(reuters.words(categories=cat)))
    return word_set


if __name__=="__main__":
    '''import data, split into essays, split lines, split into topics'''
    with open(os.path.join(data_path, 'training_set_rel3.tsv'), 'r') as f1:
        training_data = f1.read()
        training_data = training_data.split("\n")
    training_data = [t.split('\t') for t in training_data if t]
    training_data = [t for t in training_data if t != ['']]
    docs = [t[2] for t in training_data[1:]]
    print('Tokenizing documents...')
    tokens = [nltk.wordpunct_tokenize(d) for d in docs]
    print('Making lowercase...')
    tokens = makeLower(tokens)
    print('Making word_set...')
    word_set = makeWordSet()
    print('Getting real-word fractions...')
    RWFracs = getRWFrac(tokens, word_set)

    print('Saving file...')
    '''Output single file with data'''
    with open(os.path.join(data_path, 'docs_realwordfracs.txt'), 'w') as f1:
              f1.write('Doc ID' + '\t' +\
                       'Doc Type' + '\t' +\
                       'Score' + '\t'+\
                       'Frac' + '\n')
              for i in RWFracs.keys():
                  temp = [training_data[i+1][0],
                          training_data[i+1][1],
                          training_data[i+1][6],
                          str(RWFracs[i])]
                  f1.write('\t'.join(temp) + '\n')
