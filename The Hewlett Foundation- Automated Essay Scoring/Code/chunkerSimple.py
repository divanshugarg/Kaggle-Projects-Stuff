def simpleSplitter(w,t,start,current_phrase):
    if t=='PRO':
        # look for Prep, Det, Punc, unless encounter cnj
        if current_phrase and start not in ['CNJ', 'P']:
            print current_phrase
            current_phrase = ''
        current_phrase += ' ' + w
        start = t
    elif t.startswith('PRO'):
        if current_phrase and start not in ['CNJ', 'P', '', 'PRO']:
            print current_phrase
            current_phrase = ''
        current_phrase += ' ' + w
        start = t
    elif t=='P':
        # look for P, Punc
        if current_phrase and start not in ['THAT', 'P', 'WH']:
            print current_phrase
        current_phrase = w
        start = t
    elif w.lower().strip()=='that':
        print current_phrase
        print 'that'
        current_phrase = ''
        start = 'PRO'
    elif t=='CNJ':
        start = t
        current_phrase += ' ' + w
    elif w in punc_keep:
        print current_phrase
        start = '$'
        current_phrase = ''
    elif w in wh_keep:
        if start=='$':
            print w
            current_phrase = ''
            start = ''
        elif start not in ['DET']:
            #WH word in the middle of a sentence
            print current_phrase
            start = 'WH'
            current_phrase = w
        else:
            current_phrase += ' ' + w
    elif t=='DET':
        current_phrase += ' ' + w
        start = 'DET'
    else:
        current_phrase += ' ' + w
    return current_phrase, start


def isNoun(word):
    '''Call to isNumber at some point in here'''
    noun_start_list = ["'", '$', '*', '+', '-', '/']
    noun_stop_list = ['%']
    noun_keep = [n for n in noun_keep if not re.search(r'[0-9]', n)]

def isNumber(word):
    '''
    checks to see if word looks like a number, returns T or F; matching some
    of these clearly makes it a number, but stuff like "four" and "nine" may
    be subparts of non-numeric words; I think this is only needed if "of"
    is encountered; include co-ordinates, set lists, math crap, etc, etc;
    '''
    num_list = ['one', 'two', 'three', 'four', 'five',
                'six', 'seven', 'eight', 'nine', 'ten',
                'eleven', 'twelve', 'thirteen', 'fourteen',
                'fifteen',
    tens = ['twenty', 'thirty', 'fourty']
    mags = ['hundred', 'thousand', 'million', 'billion']
                
current_phrase = ''
start = '$'
index = 0
while index < len(test):
    w,t = test[index]
    current_phrase, start = simpleSplitter(w,t,start,current_phrase)
    index += 1
