import sys, os
import random

import nltk

type1 = random.sample(range(1783), 50)  #1783 is num of type1 docs
docs_type1_FD = nltk.FreqDist()
for k in type1:
    docs_type1_FD.update(tokens[k])     # tokens as from len metrics shit
docs_type1_FD.plot(30, cumulative=True)

'''making all texts into a single tokenized-text-list'''
docs = [t[2] for t in training_data]
docs = [d.strip('"') for d in docs]
texts = [d.replace('@', '') for d in docs]
texts = [nltk.wordpunct_tokenize(t) for t in texts]
text = list()
for t in texts:
    text.extend(t)
'''This is essentially a modified (controllable) concordance'''
mon_matches = [i for i,j in enumerate(text)\
               if j.startswith("MONTH")]
for k in random.sample(mon_matches, 20):
	print text[k-1:k+2]


from nltk.corpus import brown

# this sample works:
trigram_counts = nltk.defaultdict(int())
temp = brown.tagged_sents(categories='adventure')
for sent in temp:
    for (w1,t1),(w2,t2),(w3,t3) in nltk.trigrams(sent):
	trigram_counts[(t1,t2,t3)] += 1


with open('/Users/sinn/Kaggle-Projects-Stuff/The Hewlett Foundation- Automated Essay Scoring/Data-Generated/essay08_byScores.txt', 'w') as f1:
	for s in score_values:
		targets = scores[str(s)]
		temp_str_out = str()
		for d in docs:
			if d[0] in targets:
				temp_str_out += d[2]+'\n\n'
		f1.write(str(s) + '\n' + temp_str_out + '\n')
