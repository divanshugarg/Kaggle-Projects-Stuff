import sys, os
import random
import math

import nltk
from nltk.corpus import brown

from basic_data_inout import loadTrainingData
from basic_parsing import run_parse
from save_loadTaggedDocs import cTagToStr

'''Trying to find frequency of trigram tags...'''
tri_default_prob = -15      # based on range of about -4 to about -14...
bi_default_prob = -12
data_path = '/Users/sinn/Documents/Kaggle/The Hewlett Foundation- Automated Essay Scoring'
sample_name = 'Full08_docsProbDict_both'


def getNgramsCorpus(corpus, n=3, simple_tags=False):
    '''
    Really n is just 2 or 3, and corpus can be any standard corpus, or any list
    of docs with attributes "categories" and tagged data;
    '''
    ngram_counts    = nltk.defaultdict(int)
    count           = 0
    for sent in corpus.tagged_sents(categories=corpus.categories(),
                                   simplify_tags=simple_tags):
        if n==3:
            for (w1,t1),(w2,t2),(w3,t3) in nltk.trigrams(sent):
                ngram_counts[(t1,t2,t3)] += 1
                count += 1
        elif n==2:
            for (w1,t1),(w2,t2) in nltk.bigrams(sent):
                ngram_counts[(t1,t2)] += 1
                count += 1
    return ngram_counts, count
    '''frac_rep = float(len(trigram_counts.keys()))/count ~= 0.054'''

def processTextsSample(docs, k=50):
    '''Takes subset of docs and runs through seg-split-tagging'''
    if k < len(docs):
        index_doc_sub   = random.sample(range(len(docs)), k)
    else:
        index_doc_sub   = range(len(docs))
    docs_sub            = [docs[i] for i in index_doc_sub]
    docs_sub_tag        = run_parse(docs_sub)
    return index_doc_sub, docs_sub_tag

def calcLogProbsRef(ngrams_ref):
    '''Turn the ngram count dict into an ngram log-prob dict'''
    total       = sum(ngrams_ref.values())
    logProbDict = dict()
    for key in ngrams_ref.keys():
        logProbDict[key] = math.log(float(ngrams_ref[key])/total)
    return logProbDict

def calcDocsProbs(docs, NGramProbDict):
    '''Calcs prob of each doc based on found ngram tags in doc, returns dict'''
    docsProbDict = dict()
    for i,doc in enumerate(docs):
        docsProbDict[i] = calcDocProb(doc, NGramProbDict)
    return docsProbDict

def calcDocProb(doc, NGramProbDict):
    '''
    Gets the total probability of a document by summing thelog probabilities
    of sentences
    '''
    n       = len(NGramProbDict.keys()[0])
    prob    = 0.0
    count   = 0
    for sent in doc:
        prob += calcSentProb(sent, NGramProbDict, n)
        count += 1
    return float(prob) / count

def calcSentProb(sent, NGramProbDict, n):
    '''
    Look up each tag-ngram (trigrams here) in the target sentence in the
    ngrams log-prob dictionary; if found, add log-prob to total, else use
    the default prob;
    '''
    prob    = 0.0
    count   = 0
    if len(sent)< 2:
        prob = -12
        count = 1
    elif len(sent)<3 or n==2:
        for (w1,t1),(w2,t2) in nltk.bigrams(sent):
            if (t1,t2) in NGramProbDict.keys():
                prob += NGramProbDict[(t1,t2)]
            else:
                prob += tri_default_prob
            count += 1
    elif n==3:
        for (w1,t1),(w2,t2),(w3,t3) in nltk.trigrams(sent):
            if (t1,t2,t3) in NGramProbDict.keys():
                prob += NGramProbDict[(t1,t2,t3)]
            else:
                prob += bi_default_prob
            count += 1
    return float(prob) / count

if __name__=="__main__":
    print('Grabbing docs...')
    docs                        = loadTrainingData()
    docs                        = [d for d in docs if d[1]=='8']
    texts                       = [d[2].strip('"') for d in docs[1:]]
    print('Processing text...')
    index_doc_sub, docs_sub_tag = processTextsSample(texts, k=len(texts))
    print('Saving tagged docs...')
    string_version = cTagToStr(docs_sub_tag)
    with open(os.path.join(data_path, sample_name+'taggedDocs.txt'), 'w') as f1:
                f1.write(string_version)
    print('Building reference dict...')
    bigram_counts, bicount      = getNgramsCorpus(brown, n=2)
    trigram_counts, tricount    = getNgramsCorpus(brown, n=3)
    bilogProbDict               = calcLogProbsRef(bigram_counts)
    trilogProbDict              = calcLogProbsRef(trigram_counts)
    print('Calculating doc probs...')
    bidocsProbDict              = calcDocsProbs(docs_sub_tag, bilogProbDict)
    tridocsProbDict             = calcDocsProbs(docs_sub_tag, trilogProbDict)
    print('Saving file...')
    with open(os.path.join(data_path, sample_name+'probs.txt'), 'w') as f1:
        f1.write('DocIndex' + '\t' + \
                 'BiDocProb' + '\t' + \
                 'TriDocProb' + '\t' +\
                 'DocScore' + '\t' + \
                 'DocType' + '\n')
        for i,j in enumerate(index_doc_sub):
            temp = [str(j),
                    str(bidocsProbDict[i]),
                    str(tridocsProbDict[i]),
                    str(docs[j][6]),
                    str(docs[j][1])]
            f1.write('\t'.join(temp) + '\n')
