import os, sys

from basic_data_inout import loadTrainingData
from basic_parsing import run_parse
from save_loadTaggedDocs import cTagToStr

data_path = '/Users/sinn/Kaggle-Projects-Stuff/The Hewlett Foundation- Automated Essay Scoring/Data-Generated'
sample_name = 'Full01-07_docsProbDict_both'


if __name__=="__main__":
    print('Commence tag and bag...')
    print('Grabbing documents...')
    docs = loadTrainingData()
    docs = [d for d in docs if d[1]!='8']
    docs = docs[1:]
    texts = [d[2] for d in docs]
    print('Processing texts...')
    docs_tag = run_parse(texts)
    print('Saving tagged docs...')
    string_version = cTagToStr(docs_tag)
    with open(os.path.join(data_path, sample_name+'_taggedDocs.txt'), 'w') as f1:
        f1.write(string_version)
    print('Finished tagging and bagging...')
