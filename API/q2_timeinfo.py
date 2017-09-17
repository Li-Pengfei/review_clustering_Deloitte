import nltk
import re
def extract_am(word_list):
    if 'am' in word_list:
        amidxs = [i for i,val in enumerate(word_list) if val=='am']
        time_nn = []
        #print len(amidxs)
        for amidx in amidxs:
            time_slot = []
            idx_start = max(amidx-2, 0)
            for ix in range(idx_start, amidx):
                if word_list[ix].isdigit():
                    time_slot.append(word_list[ix])
            if len(time_slot) == 2:
                time_value = float(time_slot[0])+int(time_slot[1])/60.0
                time_nn.append(time_value)
            if len(time_slot) == 1:
                time_nn.append(float(time_slot[0]))
        if time_nn:
            return min(time_nn)
        else:
            return None

def extract_pm(word_list):
    if 'pm' in word_list:
        amidxs = [i for i,val in enumerate(word_list) if val=='pm']
        time_nn = []
        #print len(amidxs)
        for amidx in amidxs:
            time_slot = []
            idx_start = max(amidx-2, 0)
            for ix in range(idx_start, amidx):
                if word_list[ix].isdigit():
                    time_slot.append(word_list[ix])
            if len(time_slot) == 2:
                time_value = int(time_slot[0])+int(time_slot[1])/60.0
                time_nn.append(float(time_value))
            if len(time_slot) == 1:
                time_nn.append(float(time_slot[0]))
        if time_nn:
            #print word_list
            return max(time_nn)
        else:
            return None

def time_extract(sen):
    word_list = nltk.word_tokenize(sen[0])
    clean_word_list = []
    for word in word_list:
        clean_word_list = clean_word_list + filter(None, re.split('(-|:|am|pm)', word)) 
    return (extract_am(clean_word_list), extract_pm(clean_word_list))

def day_extract(sen): 
    word_list = nltk.word_tokenize(sen[0])
    class_0 = ['sunday', 'sundays']
    class_1 = ['weekend', 'weekends']
    class_2 = ['holidays', 'holiday']
    if not set(word_list).isdisjoint(class_0):
        return class_0[0]
    if not set(word_list).isdisjoint(class_1):
        return class_1[0]
    if not set(word_list).isdisjoint(class_2):
        return class_2[0]