'''
Code for saving and loading tagged documents; prserve layers of document, when
present;
'''
import re

def cTagToStr(docs):
    '''Takes tagged docs and converts to a list of strings to be saved to file'''
    new_string = str()
    for doc in docs:
        new_string += '<doc>\n'
        new_string += cTDocToStr(doc)
        new_string += '</doc>\n'
    return new_string

def cStrToTag(raw):
    '''
    Takes a string in the format created by cTagToStr and creates a list of
    tagged ducuments separated into structures as specified by string
    '''
    new_docs = list()
    docs = re.split('</doc>\n', raw)
    docs = [d for d in docs if d]
    docs = [d.strip('<doc>\n') for d in docs]
    for string in docs:
        new_docs.append(cStrToTDoc(string))    
    return new_docs

def cTDocToStr(doc, layer=1):
    '''Converts a tagged element to a structured string for output to file'''
    new_string = str()
    if type(doc[0])==list:
        '''Down another layer in the doc'''
        for s in doc:
            if layer==1: new_string += '\t<sent>\n'
            else:
                new_string += '\t'*layer + '<lay' + str(layer) + '>\n'
            new_string += cTDocToStr(s, layer+1)
            if layer==1: new_string += '\t</sent>\n'
            else:
                new_string += '\t'*layer + '</lay' + str(layer) + '>\n'
        return new_string
    elif type(doc[0])==tuple:
        '''Bottomed out at tagged tuples of words'''
        new_string += '\t'*layer
        word_string = str()
        tags_string = str()
        for (w1,t1) in doc:
            word_string += w1 + '  '
            tags_string += t1 + '  '
        new_string += word_string + '\n' + '\t'*layer + tags_string +'\n'
        return new_string
    else:
        raise AttributeError, 'document has bad form'

def cStrToTDoc(string, layer=1):
    new_doc = list()
    string = string.strip('\t'*layer)
    if string.startswith('<sent>'):
        docs = re.split('</sent>\n', string)
        docs = [d.strip('<sent>\n') for d in docs]
        for i,d in enumerate(docs):
            docs[i] = cStrToTDoc(d, layer=layer+1)
        return docs
    elif string.startswith('<lay' + str(layer)):
        docs = re.split('</lay' + str(layer) + '>\n')
        docs = [d.strip('<lay' + str(layer) + '>\n') for d in docs]
        for i,d in enumerate(docs):
            docs[i] = cStrToTDoc(d, layer=layer+1)
        return docs
    else:
        words_tags = string.split('\n')
        words_tags[1] = words_tags[1].strip('\t'*layer)
        words_tags = zip(re.split('  ', words_tags[0]),
                         re.split('  ', words_tags[1]))
        return words_tags

    
