'''
A general string doc to tagged pos doc; the main functions expect a list of
documents as input having had the previous operation alread performed (i.e.,
the word tokenizer expectes the documents to have already been parsed into
sentences, etc.);
'''
import sys, os

import nltk


def run_parse(docs):
    print docs[0][:20]
    docs = sent_seg(docs)
    print docs[0][1]
    docs = word_tokenize(docs)
    print docs[0][1]
    docs = pos_tagging(docs)
    print docs[0][1]
    return docs

def sent_seg(docs):
    '''Docs is list of string documents; just use default for now'''
    for i,d in enumerate(docs):
        d = sentSeg(d)
        docs[i] = d
    return docs

def word_tokenize(docs):
    '''
    Docs is a list of sentence-segmented documents; again, just basic stuff
    for now;
    '''
    for i,d in enumerate(docs):
        for k,s in enumerate(d):
            s = wordTok(s)
            d[k] = s
        docs[i] = d
    return docs

def pos_tagging(docs):
    '''
    Docs is now a list of sentences that are lists of words
    '''
    for i,d in enumerate(docs):
        d = nltk.batch_pos_tag(d)
##        for k,s in enumerate(d):
##            s = posTags(s)
##            d[k] = s
        docs[i] = d
    return docs


def sentSeg(doc):
    '''Handles doc->sent parsing'''
    doc = nltk.sent_tokenize(doc)
    return doc

def wordTok(sent):
    '''Handles sent->word parsing'''
    sent = nltk.word_tokenize(sent)
    sent = [w for w in sent if w not in ['@']]
    return sent

def posTags(sent):
    '''Handles (sent of words)->(sent of pos tagged words)'''
    sent = nltk.pos_tag(sent)
    return sent
