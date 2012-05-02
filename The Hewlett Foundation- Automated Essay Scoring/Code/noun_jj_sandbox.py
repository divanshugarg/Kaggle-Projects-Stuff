import sys, os, re

sys.path.append('/Users/sinn/Kaggle-Projects-Stuff/The Hewlett Foundation- Automated Essay Scoring/Code')

import save_loadTaggedDocs

with open('/Users/sinn/Kaggle-Projects-Stuff/The Hewlett Foundation- Automated Essay Scoring/Data-Generated/Full08_docsProbDict_both_taggedDocs.txt', 'r') as f1:
    raw = f1.read()

tagged_08 = save_loadTaggedDocs.cStrToTag(raw)
tagged_08[1][0] = [tagged_08[1][0]]
temp = list()
for s in tagged_08[1]:
    short_list = list()
    count = 0
    for (w1,t1) in s[0]:
        '''Nouns, pronouns, adjectives...'''
	if re.search(r'NN|PRP|JJ',t1):
	    short_list.append((str(count),w1))
	    count = 0
	else: count += 1
    temp.append(short_list)

spacing = [w for s in temp for w,t in s]
spacing = spacing[1:]+['None']
count = 0
words_phrases = list()
for s in temp:
    temp_wp = ''
    for s,w in s:
	temp_wp += w + ' '
	if spacing[count]!='0':
	    words_phrases.append(temp_wp)
	    temp_wp = ''
	count += 1
