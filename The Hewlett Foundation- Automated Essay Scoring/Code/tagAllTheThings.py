import os, sys

from basic_data_inout import loadTrainingData
from basic_parsing import run_parse
from save_loadTaggedDocs import cTagToStr



if __name__=="__main__":
    print('Commence tag and bag...')
    print('Grabbing documents...')
    docs = loadTrainingData()
    docs = [d for d in docs if d[1]!='8']
    texts = [d[2] for d in docs]
    print('Processing texts...')
    index_doc_sub, docs_sub_tag = processTextsSample(texts, k=len(texts))
    print('Saving tagged docs...')
        string_version = cTagToStr(docs_sub_tag)
        with open(os.path.join(data_path, sample_name+'taggedDocs.txt'), 'w') as f1:
                    f1.write(string_version)
    print('Finished tagging and bagging...')
