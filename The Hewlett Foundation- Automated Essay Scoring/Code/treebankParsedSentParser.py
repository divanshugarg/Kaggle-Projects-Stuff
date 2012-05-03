def getAllTagTypes(parsed_sents):
    tag_set = set()
    for sent in parsed_sents:
        sent = str(sent)
        sent = sent.replace('\n', '')
        sent = sent.split('(')
        sent = [w.strip() for w in sent if w.strip()]
        tag = [w.split(' ')[0] for w in sent]
        tag_set = tag_set.union(set(tag))
    tag_list = list(tag_set)
    tag_set = set()
    for t in tag_list:
        if re.search(r'[0-9]+', t):
            if t.find('=')>=0:
                t = t.split('=')[0]
            else:
                t = '-'.join(t.split('-')[:-1])
        tag_set.add(t)
    return tag_set

'''
Find all the NP's and VP's, see what they start with / end with, and see what
kind of phrase comes before them
'''
def getStartEnd(parsed_sents):
    se_dict = dict()
    se_dict['NP'] = nltk.defaultdict(int)
    se_dict['VP'] = nltk.defaultdict(int)
    for sent in parsed_sents:
        checkSE(sent)


def navTree(tree):
    '''Tree is a sent. tree; call recursive while still room to go'''
    child_nodes = [child.node for child in tree if isinstance(child, nltk.Tree)]
    new_additions = findMatches(child_nodes)
    for child in tree if isinstance(child, nltk.Tree):
        temp_additions = navTree(child)

def findMAtches(child_nodes):
    '''
    Child nodes is a list of node-type lists; grab all data regarding VP/NP
    starts/ends, etc.;
    '''
