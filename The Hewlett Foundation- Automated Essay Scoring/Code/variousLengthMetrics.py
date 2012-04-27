import sys, os

from basic_parsing import sent_seg
from basic_parsing import word_tokenize

data_path = '/Users/sinn/Documents/Kaggle/The Hewlett Foundation- Automated Essay Scoring'

def len_docs(docs):
    '''Returns num things per doc, initially | post sent_seg'''
    counts = dict()
    for i,d in enumerate(docs):
        counts[i] = len(d)
    return counts

def len_sents(docs):
    '''Returns num things per sentence per doc, post sent_seg | word_toke'''
    counts = dict()
    for i,d in enumerate(docs):
        temp = list()
        for s in d:
            temp.append(len(s))
        counts[i] = temp
    return counts

def ratios(str_lengths, ent_lengths):
    '''
    "str_lengths" are the lengths of target things in chars, while
    "ent_lengths" are the lengths of target things in parts (e.g., sents
    or words for docs, sents respectively);
    '''
    zipped_lengths = zip(str_lengths, ent_lengths)
    ratios = dict()
    for k,(i,j) in enumerate(zipped_lengths):
        ratios[k] = float(j) / i
    return ratios


if __name__=="__main__":
    '''Really a pretty simple process'''
    '''import data, split into essays, split lines, split into topics'''
    print('Opening file...')
    with open(os.path.join(data_path, 'training_set_rel3.tsv'), 'r') as f1:
        training_data = f1.read()
        training_data = training_data.split("\n")
    training_data = [t.split('\t') for t in training_data if t]
    training_data = [t for t in training_data if t != ['']]
    print('Getting docs...')
    docs = [t[2] for t in training_data[1:]]

    '''1st:  create CondFreqDist for docs:'''
    ##various_punct = ['@', '"', '.', '?', '!', ';', ':', ',']
    ##tokens = [nltk.wordpunct_tokenize(d) for d in docs]
    ##for i,t in enumerate(tokens):
    ##    t = [w.lower() for w in t if not in various_punct]
    ##    tokens[i] = t
    ##doc_token_pairs = list()
    ##for i,d in enumerate(tokens):
    ##    doc_token_pairs.extend(zip(['doc'+str(i) \
    ##                                for k in range(len(tokens[i]))],
    ##                               tokens[i]))
    ##docs_words_CDF = nltk.ConditionalFreqDist(doc_token_pairs)

    print('Starting simple stat extraction...')
    '''2nd:  get counts and meta for various features'''
    docs_lengths_chars = len_docs(docs)         # docs are strings, get len
    print('Sentence segmenting...')
    docs = sent_seg(docs)                       # docs are lists of sents
    docs_lengths_sents = len_docs(docs)         # get num sents per doc
    docs_sents_lengths_chars = len_sents(docs)  # sents are strings, get len
    print('Word tokenizing...')
    docs = word_tokenize(docs)                  # sents are lists of words
    docs_sents_lengths_words = len_sents(docs)  # get num words per sent per doc

    '''Simple summaries'''
    docs_sents_lengths_chars_avg = [float(sum(k))/len(k) for\
                                    k in docs_sents_lengths_chars.values()]

    docs_sents_lengths_words_avg = [float(sum(k))/len(k) for\
                                    k in docs_sents_lengths_words.values()]

    print('Saving file...')
    '''Output single file with data'''
    with open(os.path.join(data_path, 'docs_simple_stats.txt'), 'w') as f1:
              f1.write('Doc ID' + '\t' + 'Doc Type' + '\t' + 'Score' + '\t'+\
                       'Len Chars' + '\t' + 'Len Words' + '\t' + \
                       'Len Sents' + '\t' +  'Sents Len Chars' + '\t' + \
                       'Sents Len Words' + '\n')
              for i,d in enumerate(docs):
                  temp = [training_data[i+1][0], training_data[i+1][1],
                          training_data[i+1][6],
                          str(docs_lengths_chars[i]),
                          str(sum(docs_sents_lengths_words[i])),
                          str(docs_lengths_sents[i]),
                          str(docs_sents_lengths_chars_avg[i]),
                          str(docs_sents_lengths_words_avg[i])]
                  f1.write('\t'.join(temp) + '\n')
          
