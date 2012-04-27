import sys, os
import re

import nltk

data_path = '/Users/sinn/Documents/Kaggle/The Hewlett Foundation- Automated Essay Scoring'

def loadTrainingData(specs=None):
    '''import data, split into essays, split lines'''
    with open(os.path.join(data_path, 'training_set_rel3.tsv'), 'r') as f1:
        training_data = f1.read()
        training_data = training_data.split("\n")
    training_data = [t.split('\t') for t in training_data if t]
    training_data = [t for t in training_data if t != ['']]
    if not specs:
        return training_data

def sepEssayTypes(training_data, cats=range(1,9)):
    '''Split training set data into topics'''
    training_set_dict = dict()
    for k in range(8):
        training_set_dict[str(k+1)] = list()
    for k in training_data[1:]:
        training_set_dict[k[1]].append(k)
    return training_set_dict

if __name__=="__main__":
    '''Basic stuff'''
    # just 8th set for now...
    temp_data = [t[2] for t in training_set_dict['8']]
    temp_data = [[len(t[2])] + t[3:] for t in temp_data]
    for i,k in enumerate(temp_data):
        k[-1] = k[-1].strip('\r')
        temp_data[i] = k
    with open(os.path.join(data_path, 'set08_count_score.txt'), 'wb') as f1:
        for k in temp_data:
            k[0] = str(k[0])
            f1.write('\t'.join(k) + '\n')

    type_len_score_data = [[t[1]]+[len(t[2])]+t[3:] for t in training_data]
    for i,k in enumerate(type_len_score_data):
            k[-1] = k[-1].strip('\r')
            type_len_score_data[i] = k
    type_len_score_data = type_len_score_data[1:]
    with open(os.path.join(data_path, 'type_len_score_date.txt'), 'wb') as f1:
        for k in type_len_score_data:
            k[1] = str(k[1])
            f1.write('\t'.join(k) + '\n')

