import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk.stem.porter import PorterStemmer
import string
import re
stemmer = PorterStemmer()

def process_corpus(content, pos_tags, question):
    assert (question in range(1, 11)), "Question number must between 1-10 (inclusive)!"

    stop_words = stopwords.words('english')
    punctuation_list = [unicode(i) for i in string.punctuation]
    for punctuation in punctuation_list:
        stop_words.append(punctuation)

    # split three categories: 1 no improvemnt 2 with pos_tags words 3 others
    doc_noimprove = []
    doc_nn = []
    nn_extracted = []
    doc_other = []
    if question in [3, 5, 10]:
        for idx, review in enumerate(content):
            if 'no improvement' in review:
                doc_noimprove.append((review, idx))
            else:
                nn_list = []
                sen = review
                pos_new = nltk.pos_tag(nltk.word_tokenize(sen))
                for token in pos_new:
                    if token[1] in pos_tags and not token[0] in stop_words:
                        nn_list.append(token[0])
            # stemming
                for counter, word in enumerate(nn_list):
                    nn_list[counter] = stemmer.stem(word)
            # apply rule
                switcher = {
                    1: rule_q1, 2: rule_q2, 3: rule_q3, 4: rule_q4, 5: rule_q5, 6: rule_q6,
                    7: rule_q7, 8: rule_q8, 9: rule_q9, 10: rule_q10
                }
            # Get the corresponding rule function
                func = switcher.get(question)
            # Execute the rule function
                nn_list = func(sen, nn_list)

                if nn_list != []:
                    nn_extracted.append((nn_list, idx))
                    doc_nn.append((sen, idx))
                else:
                    doc_other.append((sen, idx))
        return doc_noimprove, [doc_nn, nn_extracted], doc_other
    elif question in [2]:
        doc_days = []
        doc_time = []
        day_senswords = ['sunday', 'sundays', 'weekend', 'weekends', 'holidays', 'holiday']

        for idx, review in enumerate(content):
            if 'no improvement' in review:
                doc_noimprove.append((review, idx))
            else:
                sents = sent_tokenize(review)
                for sen in sents:
                    word_list = nltk.word_tokenize(sen)
                    if len(word_list) > 5:
                        if not set(word_list).isdisjoint(day_senswords):
                            doc_days.append((sen, idx))
                        else:
                            clean_word_list = []
                            for word in word_list:
                                clean_word_list = clean_word_list + filter(None, re.split('(-|:|am|pm)', word)) 
                            if 'am' in clean_word_list or 'pm' in clean_word_list or any(i.isdigit() for i in clean_word_list):
                                doc_time.append((sen, idx))
                            else:
                                doc_other.append((sen, idx))
                    else:
                        continue
        return doc_noimprove, [doc_days, doc_time], doc_other       
    else:
        print "Contents with multiple sentences are splited into single sentences."
        for idx, review in enumerate(content):
            if 'no improvement' in review:
                doc_noimprove.append((review, idx))
            else:
                sents = sent_tokenize(review)
                for sen in sents:
                    nn_list = []
                    pos_new = nltk.pos_tag(nltk.word_tokenize(sen))
                    for token in pos_new:
                        if token[1] in pos_tags and not token[0] in stop_words:
                            nn_list.append(token[0])
            # stemming
                    for counter, word in enumerate(nn_list):
                        nn_list[counter] = stemmer.stem(word)
            # apply rule
                    switcher = {
                        1: rule_q1, 2: rule_q2, 3: rule_q3, 4: rule_q4, 5: rule_q5, 6: rule_q6,
                        7: rule_q7, 8: rule_q8, 9: rule_q9, 10: rule_q10
                    }
            # Get the corresponding rule function
                    func = switcher.get(question)
            # Execute the rule function               
                    nn_list = func(sen, nn_list)
                    if nn_list != []:
                        nn_extracted.append((nn_list, idx))
                        doc_nn.append((sen, idx))
                    else:
                        doc_other.append((sen, idx))
        return doc_noimprove, [doc_nn, nn_extracted], doc_other

    

def rule_q1(sen, ne):
    clean_ne = list(set(ne))
    remove_words = ["appoint", "improv", "custom", "servic", "peopl", "person", "facil", "avail", "good", \
                    "center", "centr", "car", "dealership", "vehicl", "toyota", "problem", "work", "much", \
                    "thing", "possibl", "need"]  # stemmed
    clean_ne = [word for word in clean_ne if word not in remove_words]
    save_words = ["without", "call", "wait", "pick", "pickup", "drop", "remind", "inform", "respons", "book", "fix", \
                  "receiv", "same", "sm", "immedi", "urgent", "urgenc", "deliv", "deliveri", "explain",
                  "detail"]  # stemmed
    clean_ne = clean_ne + [stemmer.stem(word) for word in sen.split() if stemmer.stem(word) in save_words]

    # rules to merge keywords:
    if 'pickup' in clean_ne:
        clean_ne[clean_ne.index('pickup')] = 'pick'
    if 'phone' in clean_ne:
        clean_ne[clean_ne.index('phone')] = 'call'
    if 'telephon' in clean_ne:
        clean_ne[clean_ne.index('telephon')] = 'call'
    if 'messag' in clean_ne:
        clean_ne[clean_ne.index('messag')] = 'sm'
    if 'km' in clean_ne:
        clean_ne[clean_ne.index('km')] = 'locat'
    if 'area' in clean_ne:
        clean_ne[clean_ne.index('area')] = 'locat'
    if 'deliveri' in clean_ne:
        clean_ne[clean_ne.index('deliveri')] = 'deliv'
    if 'urgent' in clean_ne:
        clean_ne[clean_ne.index('urgent')] = 'emerg'
    if 'urgenc' in clean_ne:
        clean_ne[clean_ne.index('urgenc')] = 'emerg'
    if 'detail' in clean_ne:
        clean_ne[clean_ne.index('detail')] = 'inform'
    if 'explain' in clean_ne:
        clean_ne[clean_ne.index('explain')] = 'inform'
    if 'should tell' in sen:
        clean_ne.append('inform')
    # add keyword "appointment"
    if 'book' in clean_ne:
        clean_ne[clean_ne.index('book')] = 'appointment'
    if 'day' in clean_ne:  # split 'day' to 'appointment' and 'wait'
        if 'appointment' in sen:
            clean_ne[clean_ne.index('day')] = 'appointment'
        elif 'days' in sen:
            clean_ne[clean_ne.index('day')] = 'wait'
        else:
            clean_ne.remove('day')
    if 'week' in clean_ne and 'appointment' in sen:
        clean_ne[clean_ne.index('week')] = 'appointment'
    if 'month' in clean_ne and 'appointment' in sen:
        clean_ne[clean_ne.index('month')] = 'appointment'
    # add keyword "without_appointment"
    if 'without appointment' in sen or 'without any appointment' in sen:
        clean_ne.append('without_appointment')
    # add keyword "on_time"
    if 'on time' in sen and 'time' in clean_ne:
        clean_ne[clean_ne.index('time')] = 'on_time'
    if 'that time' in sen and ('servic' in sen or 'work' in sen or 'attend' in sen) and 'time' in clean_ne:
        clean_ne[clean_ne.index('time')] = 'on_time'
    if 'fulfill' in sen or 'stick' in sen and 'time' in clean_ne:
        clean_ne[clean_ne.index('time')] = 'on_time'
    # split "immediately" into "wiat" and "appointment" cluster
    if 'immedi' in clean_ne:
        if 'servic' in sen or 'work' in sen or 'attend' in sen:
            clean_ne[clean_ne.index('immedi')] = 'wait'
        else:
            clean_ne[clean_ne.index('immedi')] = 'appointment'
    # split 'time' to other clusters
    if 'too much time' in sen:
        clean_ne[clean_ne.index('time')] = 'wait'
    if 'long time' in sen:
        if 'appointment' in sen:
            clean_ne[clean_ne.index('time')] = 'appointment'
        else:
            clean_ne[clean_ne.index('time')] = 'wait'
    if 'time' in clean_ne:
        if 'appointment' in sen:
            clean_ne[clean_ne.index('time')] = 'appointment'
        else:
            clean_ne.remove('time')  # remove other 'times'

    clean_ne = list(set(clean_ne))
    return clean_ne

def rule_q2(sen, ne):
    return


def rule_q3(sen, ne):
    clean_ne = list(set(ne))
    remove_words = ['custom', 'car', 'vehicl', 'servic', 'toyota', 'thing', 'good', \
                    'day', 'center', 'centr', 'dealership', 'time']  # stemmed
    clean_ne = [word for word in clean_ne if word not in remove_words]

    save_words = ['inform', 'tell', 'advis', 'understand', 'advic', 'call', 'answer', 'correct', 'guid', \
                  'train', 'suggest', 'respons', 'commit', 'solv', 'queri', 'updat', 'attend', 'deliv', \
                  'wait', 'mention', 'listen', 'resolv', 'respond', 'share', 'commun', 'confirm', \
                  'behavior', 'behav', 'properly', 'proper']  # stemmed
    clean_ne = clean_ne + [stemmer.stem(word) for word in sen.split() if stemmer.stem(word) in save_words]
    clean_ne = list(set(clean_ne))

    # rules to merge keywords:
    if 'share' in clean_ne:
        clean_ne[clean_ne.index('share')] = 'inform'
    if 'tell' in clean_ne:
        clean_ne[clean_ne.index('tell')] = 'inform'
    if 'behav' in clean_ne:
        clean_ne[clean_ne.index('behav')] = 'behavior'
    if 'advic' in clean_ne:
        clean_ne[clean_ne.index('advic')] = 'advis'
    if 'queri' in clean_ne:
        clean_ne[clean_ne.index('queri')] = 'question'
    if 'properly' in clean_ne:
        clean_ne[clean_ne.index('properly')] = 'proper'
    if 'worker' in clean_ne:
        clean_ne[clean_ne.index('worker')] = 'staff'

    # rules to split keywords:
    if 'inform' in clean_ne and 'information' in sen:
        clean_ne[clean_ne.index('inform')] = 'information'
    if 'respons' in clean_ne:
        if ('responsibility' in sen or 'responsibilities' in sen or 'responsible' in sen):
            clean_ne[clean_ne.index('respons')] = 'responsibility'
        else:
            clean_ne[clean_ne.index('respons')] = 'respond'
    if 'listen' in clean_ne:
        clean_ne[clean_ne.index('listen')] = 'respond'

    clean_ne = list(set(clean_ne))
    return clean_ne


def rule_q4(sen, ne):
    clean_ne = list(set(ne))
    remove_words = ['car', 'vehicl','improv','dealership','custom','receiv','satisfact','respond','servic','time',\
                    'innova','center','facil','feel','ok','tell','problem','pay','dealer','attent','hurri','condit',\
                    'ant','fine','deliver','get','question','deliveri','need','quality','day','side','kind','chang',\
                    'honda','visit','told','speak','ask','requir','maruti','cleanli','henc','place','area','hand',\
                    'compani','process','qualiti','care','outsid','complaint','depart','hour','wait','front','home',\
                    'centr','system']
    clean_ne = [word for word in clean_ne if word not in remove_words and len(word)>1]
    save_words = ['polish','wash','interior','extra','rupe','check','vacuum','clean','intern',
                  'insid','ac','dry','engin','inter']
    uni_words = ['mat','interior','charg']
    clean_ne = list(set(clean_ne + [stemmer.stem(word) for word in sen.split() if stemmer.stem(word) in save_words]))

    # rules to seperate keywords:
    if 'rupe' in clean_ne:
        clean_ne[clean_ne.index('rupe')] = 'charg'
    if 'rate' in clean_ne:
        clean_ne[clean_ne.index('rate')] = 'charg'        
    if 'cost' in clean_ne:
        clean_ne[clean_ne.index('cost')] = 'charg'
    if 'money' in clean_ne:
        clean_ne[clean_ne.index('money')] = 'charg'
    if 'insid' in clean_ne:
        clean_ne[clean_ne.index('insid')] = 'interior'
    if 'intern' in clean_ne:
        clean_ne[clean_ne.index('intern')] = 'interior'
    if 'window' in clean_ne:
        clean_ne[clean_ne.index('window')] = 'glass'
    if 'dirt' in clean_ne:
        clean_ne[clean_ne.index('dirt')] = 'dust'  
    if 'manag' in clean_ne:
        clean_ne[clean_ne.index('manag')] = 'staff'
    if 'advisor' in clean_ne:
        clean_ne[clean_ne.index('advisor')] = 'staff'  
    if 'supervisor' in clean_ne:
        clean_ne[clean_ne.index('supervisor')] = 'staff'  
    if 'labor' in clean_ne:
        clean_ne[clean_ne.index('labor')] = 'staff'
    if 'worker' in clean_ne:
        clean_ne[clean_ne.index('worker')] = 'staff'         
    if 'cloth' in clean_ne:
        clean_ne[clean_ne.index('cloth')] = 'dri'
    if 'vacuum' in clean_ne:
        clean_ne[clean_ne.index('vacuum')] = 'dri'        
    if 'water' in clean_ne:
        clean_ne[clean_ne.index('water')] = 'clean'
    if 'spot' in clean_ne:
        clean_ne[clean_ne.index('spot')] = 'stain'          
    if 'wash' in clean_ne:
        clean_ne[clean_ne.index('wash')] = 'clean'
    # rules for multi-keywords case
    if len(clean_ne) > 1 and 'dust' in clean_ne:
        clean_ne.remove('dust')
    if len(clean_ne) > 1 and 'clean' in clean_ne:
        clean_ne.remove('clean')
        
    uniwrd = [cn for cn in clean_ne if cn in uni_words]
    if uniwrd != []:
        clean_ne = uniwrd
    clean_ne = list(set(clean_ne))
    return clean_ne

def rule_q5(sen, ne):
    return

def rule_q6(sen, ne):
    clean_ne = list(set(ne))
    remove_words = ['dealership', 'locat', 'servic', 'center', 'car', 'place', 'custom', 'toyota', \
                    'facil', 'time', 'problem', 'centr', 'home', 'side', 'vehicl', 'peopl', 'lot', 'compani', \
                    'day', 'area', 'dealer']  #stemmed
    clean_ne = [word for word in clean_ne if word not in remove_words]

    save_words = ["pick", 'pickup', 'drop', 'insid', 'outsid', 'eat']  # stemmed
    clean_ne = clean_ne + [stemmer.stem(word) for word in sen.split() if stemmer.stem(word) in save_words]
    clean_ne = list(set(clean_ne))

    # rules to merge keywords:
    if 'out side' in sen:
        clean_ne.append('outside')
    if 'high way' in sen:
        if 'way' in clean_ne:
            clean_ne[clean_ne.index('way')] = 'highway'
        else:
            clean_ne.append('highway')
    if 'pickup' in clean_ne:
        clean_ne[clean_ne.index('pickup')] = 'pick'
    if 'busstop' in clean_ne:
        clean_ne[clean_ne.index('busstop')] = 'bu'
    if 'buse' in clean_ne:
        clean_ne[clean_ne.index('buse')] = 'bu'
    if 'eat' in clean_ne:
        clean_ne[clean_ne.index('eat')] = 'food'
    if 'canteen' in clean_ne:
        clean_ne[clean_ne.index('canteen')] = 'food'
    if 'kilomet' in clean_ne:
        clean_ne[clean_ne.index('kilomet')] = 'km'
    if 'market' in clean_ne:
        clean_ne[clean_ne.index('market')] = 'shop'
    if 'shop' in clean_ne and ('dealership shop' in sen or 'work shop' in sen):
        clean_ne[clean_ne.index('shop')] = 'workshop'

    clean_ne = list(set(clean_ne))
    return clean_ne


def rule_q7(sen, ne):
    clean_ne = list(set(ne))
    remove_words = ['custom','wait','car','facil','dealership','toyota','center',\
                    'room','improv','servic','arrang','owner','peopl','time']
    clean_ne = [word for word in clean_ne if word not in remove_words and len(word)>1]    
    save_words = ['clean','cleanli']
    clean_ne = list(set(clean_ne + [stemmer.stem(word) for word in sen.split() if stemmer.stem(word) in save_words]))
    if len(clean_ne) > 1 and 'area' in clean_ne:
        clean_ne.remove('area')
    if len(clean_ne) < 2 and 'area' in clean_ne:
        clean_ne[clean_ne.index('area')] = 'space'
    if 'place' in clean_ne:
        clean_ne[clean_ne.index('place')] = 'space'
    if 'chair' in clean_ne:
        clean_ne[clean_ne.index('chair')] = 'seat'
    if 'sofa' in clean_ne:
        clean_ne[clean_ne.index('sofa')] = 'seat'
    if 'coffe' in clean_ne:
        clean_ne[clean_ne.index('coffe')] = 'drink'
    if 'water' in clean_ne:
        clean_ne[clean_ne.index('water')] = 'drink'
    if 'tea' in clean_ne:
        clean_ne[clean_ne.index('tea')] = 'drink'         
    if 'clean' in clean_ne:
        clean_ne[clean_ne.index('clean')] = 'cleanli'
    if 'canteen' in clean_ne:
        clean_ne[clean_ne.index('canteen')] = 'food'
    return clean_ne

def rule_q8(sen, ne):
    return

def rule_q9(sen, ne):
    clean_ne = list(set(ne))
    remove_words = ['car', 'vehicl','improv','dealership','custom','receiv','satisfact','respond','servic','time',
                    'center','facil','feel','ok','tell','problem','pay','dealer','attent','hurri','condit','ant',
                    'fine','deliver','get','question','deliveri','need','quality','day','amount','kind','chang',
                    'honda','visit','told','speak','ask','requir','toyota','henc','place','area','filter','align',
                    'compani','process','qualiti','care','outsid','complaint','manag','glass','inform','break','pad',
                    'wash','clean','water','showroom','staff','month','year','side','break','oil','market','batteri',
                    'pack','packag','product']
    clean_ne = [word for word in clean_ne if word not in remove_words and len(word)>1]    
    save_words = ['spare','reduc','reason','discount','extra','rupe','compar','differ','pay','payment','ac','part',
                  'check','free','increas','high','low','less','more','costli','decreas','insur','explain']
    clean_ne = list(set(clean_ne + [stemmer.stem(word) for word in sen.split() if stemmer.stem(word) in save_words]))
    
    # rules to merge keywords:
    if 'rupe' in clean_ne:
        clean_ne[clean_ne.index('rupe')] = 'charg'
    if 'price' in clean_ne:
        clean_ne[clean_ne.index('price')] = 'charg'        
    if 'differ' in clean_ne:
        clean_ne[clean_ne.index('differ')] = 'compar'        
    if 'rate' in clean_ne:
        clean_ne[clean_ne.index('rate')] = 'charg'
    if 'pay' in clean_ne:
        clean_ne[clean_ne.index('pay')] = 'charg' 
    if 'payment' in clean_ne:
        clean_ne[clean_ne.index('payment')] = 'charg'         
    if 'cost' in clean_ne:
        clean_ne[clean_ne.index('cost')] = 'charg'
    if 'amount' in clean_ne:
        clean_ne[clean_ne.index('amount')] = 'charg'
    if 'bill' in clean_ne:
        clean_ne[clean_ne.index('bill')] = 'charg'           
    if 'money' in clean_ne:
        clean_ne[clean_ne.index('money')] = 'charg'
    if 'low' in clean_ne:
        clean_ne[clean_ne.index('low')] = 'reduc'
    if 'decreas' in clean_ne:
        clean_ne[clean_ne.index('decreas')] = 'reduc' 
    if 'less' in clean_ne:
        clean_ne[clean_ne.index('less')] = 'reduc'  
    if 'taxation' in clean_ne:
        clean_ne[clean_ne.index('taxation')] = 'tax'
    if 'more' in clean_ne:
        clean_ne[clean_ne.index('more')] = 'costli'
    if 'increas' in clean_ne:
        clean_ne[clean_ne.index('increas')] = 'costli'
    if 'increa' in clean_ne:
        clean_ne[clean_ne.index('increa')] = 'costli'        
    if 'high' in clean_ne:
        clean_ne[clean_ne.index('high')] = 'costli'
    if 'explain' in clean_ne:
        clean_ne[clean_ne.index('explain')] = 'explan'   
    if 'bumper' in clean_ne:
        clean_ne[clean_ne.index('bumper')] = 'spare'
    if 'part' in clean_ne:
        clean_ne[clean_ne.index('part')] = 'spare'        
    if 'tire' in clean_ne:
        clean_ne[clean_ne.index('tire')] = 'spare'        
    if 'ac' in clean_ne:
        clean_ne[clean_ne.index('ac')] = 'spare'        
    if 'vat' in clean_ne:
        clean_ne[clean_ne.index('vat')] = 'tax'
    if 'offer' in clean_ne:
        clean_ne[clean_ne.index('offer')] = 'discount'        
    clean_ne = list(set(clean_ne))

    if len(clean_ne)>1 and 'costli' in clean_ne:
        clean_ne.remove('costli')
    if len(clean_ne)>1 and 'reduc' in clean_ne:
        clean_ne.remove('reduc')
    if len(clean_ne)>1 and 'charg' in clean_ne:
        clean_ne.remove('charg')
    if len(clean_ne)==1 and 'costli' in clean_ne:
        clean_ne = ['charg']
    if len(clean_ne)==1 and 'reduc' in clean_ne:
        clean_ne = ['charg']
    if 'tax' in clean_ne:
        clean_ne= ['tax']
    if 'labor' in clean_ne:
        clean_ne= ['labor']        
    if 'spare' in clean_ne:
        clean_ne= ['spare']        
    clean_ne = list(set(clean_ne))
    return clean_ne

def rule_q10(sen, ne):
    return