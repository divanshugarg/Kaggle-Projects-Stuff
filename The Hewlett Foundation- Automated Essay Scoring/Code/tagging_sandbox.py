import sys, os
import re

import nltk

data_dir = '/Users/sinn/Kaggle-Projects-Stuff/The Hewlett Foundation- Automated Essay Scoring/Data-Generated')
code_dir = '/Users/sinn/Kaggle-Projects-Stuff/The Hewlett Foundation- Automated Essay Scoring/Code')


word_tag_dict = nltk.defaultdict(set)
word_count_dict = nltk.defaultdict(int)
for w,t in brown.tagged_words(simplify_tags=True):
    word_tag_dict[w.lower()].add(t)
    word_count_dict[w.lower()] += 1
single_tag_words = list()
for w in word_tag_dict.keys():
    if len(word_tag_dict[w])==1 and word_count_dict[w] >= 10:
        single_tag_words.append(w)

'''Pronoun stuff...'''
pro_dict = nltk.defaultdict(int)
for w,t in brown.tagged_words(simplify_tags=True):
    if t=='PRO':
	pro_dict[w.lower()] += 1
PRO = [p for p in pro_dict.keys() if pro_dict[p]>=10]
PRO = [p for p in PRO if not re.search(r"'ll|'d|'ve|'re|'s|'m", p)]

'''Determiner stuff'''
det_dict = nltk.defaultdict(int)
for w,t in brown.tagged_words(simplify_tags=True):
    if t=='DET':
	    det_dict[w.lower()] += 1
DET = [d for d in det_dict.keys() if det_dict[d]>=10]
DET = [d for d in DET if not re.search(r"'ll|'d|'ve|'re|'s|'m", d)]

'''Preposition stuff'''
prep_dict = nltk.defaultdict(int)
for w,t in brown.tagged_words(simplify_tags=True):
    if t=='P':
	prep_dict[w.lower()] += 1
PREP = [p for p in prep_dict.keys() if prep_dict[p]>=10]

'''wh-word stuff; these are pretty useful, actually...'''
wh_dict = nltk.defaultdict(int)
for w,t in brown.tagged_words(simplify_tags=True):
    if t=='WH':
        wh_dict[w.lower()] += 1
WH = [w for w in wh_dict.keys() if wh_dict[w]>=10]
WH = [w for w in WH if not re.search(r"'ll|'d|'ve|'re|'s|'m", w)]

'''noun stuff; lots of post-processing here...'''
noun_dict = nltk.defaultdict(int)
for w,t in brown.tagged_words(simplify_tags=True):
    if t=='N':
	noun_dict[w.lower()] += 1

'''
Little different here; mis-spellings are really only low-occurance words here,
and just want to make sure mis-spelling isn't another real english word'''
conj_dict = nltk.defaultdict(int)
for w,t in brown.tagged_words(simplify_tags=True):
    if t=='CNJ':
        conj_dict[w.lower()] += 1
CONJ = [c for c in conj_dict.keys() if conj_dict[c]>=10 \
        or len(all_tagged_word_counts[c])==1]

overlap = set(DET).intersection(set(PRO))   # just 'them' when misused (them apples)


'''Pain in the ass, but prob needs to be done...takes no time now :)'''
all_tagged_word_counts = nltk.defaultdict(lambda: nltk.defaultdict(int))
for w,t in brown.tagged_words(simplify_tags=True):
    all_tagged_word_counts[w.lower()][t] += 1
##'''takes forever to make, pickle it..'''
##out_dir = os.path.join(data_dir, 'brown_tagged_word_counts.pkl')
##pickle.dump(all_tagged_word_counts, open(out_dir, 'w'))

'''Get words that occur >= 10 times'''
all_tagged_word_counts_frequent = set()
for w in all_tagged_word_counts:
    count = sum(all_tagged_word_counts[w].values())
    if count >= 10:
        all_tagged_word_counts_frequent.add(w)

'''Just as a check; significantly reduces DET & PREP, moderately reduces PRO'''
T = 0.9

det_keep = [d for d in DET if \
            float(det_dict[d]) / \
            sum(all_tagged_word_counts[d].values())>=T]
len(det_keep)==len(DET)

pro_keep = [p for p in PRO if \
            float(pro_dict[p]) / \
            sum(all_tagged_word_counts[p].values())>=T]
len(pro_keep)==len(PRO)

prep_keep = [p for p in PREP if \
             float(prep_dict[p]) / \
             sum(all_tagged_word_counts[p].values())>=T]
len(prep_keep)==len(PREP)

conj_keep = [c for c in CONJ if \
             float(conj_dict[c]) / \
             sum(all_tagged_word_counts[c].values())>=T]
len(conj_keep)==len(CONJ)

wh_keep = [w for w in WH if \
           float(wh_dict[w]) / \
           sum(all_tagged_word_counts[w].values())>=T]
len(wh_keep)==len(WH)

noun_keep = [n for n in noun_dict.keys() if \
             float(noun_dict[n]) / \
             sum(all_tagged_word_counts[n].values()) >= T]
noun_keep = [n for n in noun_keep if not \
             re.search(r"[0-9]|'|\$|\*|\+|/|\%|#", n)]
noun_keep = [n for n in noun_keep if not n.startswith('-')]
len(noun_keep)==len(noun_dict)

'''
Get list of words that have been removed from prep, pro, det; should this
be only words not still occuring in these lists;
'''
throw_aways = list()
throw_aways.extend(list(set(PREP).difference(prep_keep)))
throw_aways.extend(list(set(PRO).difference(pro_keep)))
throw_aways.extend(list(set(DET).difference(det_keep)))
throw_aways = list(set(throw_aways))

'''Separating by properties...'''
pro_poss_keep = [w for w,t in nltk.pos_tag(pro_keep) if t=='PRP$']
pro_keep = list(set(pro_keep).difference(pro_poss_keep)).append('his') #
'''his is both...because of this, do pro_poss_keep 1st, eval & change if nec?'''

'''Tag the basic stuff'''
for w in temp_words:
    if w.lower() in prep_keep:
        new = (w, 'P')
    elif w.lower() in pro_poss:
        new = (w, 'PRO$')
    elif w.lower() in pro_keep:
        new = (w, 'PRO')
    elif w.lower() in det_keep:
        new = (w, 'DET')
    elif w.lower() in conj_keep:
        new = (w, 'CNJ')
    elif w.lower() in noun_keep:
        new = (w, 'NN')
    elif w.lower() in wh.keep:
        new = (w, 'WH')
    else: new = (w, '')
    temp_tagged_words.append(new)
