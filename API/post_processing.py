from collections import Counter
import heapq
from cluster_centroid import get_Cluster_Centroid

def df_count_tuple(corpus):
    text = []
    for comment in corpus:
        text = text + comment[0]
    df = Counter(text)
    return df

def df_count(corpus):
    text = []
    for comment in corpus:
        text = text + comment
    df = Counter(text)
    return df

def filter_ne(corpus, doc_nn, df, question):  # assuming each review contain one aspect
    assert (question in range(1, 11)), "Question number must between 1-10 (inclusive)!"
    # function mapping
    switcher = {
        1: filter_rule_q1, 2: filter_rule_q2, 3: filter_rule_q3, 4: filter_rule_q4, 5: filter_rule_q5, 6: filter_rule_q6,
        7: filter_rule_q7, 8: filter_rule_q8, 9: filter_rule_q9, 10: filter_rule_q10
    }
    func = switcher.get(question)

    corpus_keyword = []
    for idx, doc in enumerate(corpus):
        if len(doc[0]) > 1:
            apply_rule = func(doc[0], idx, corpus_keyword, doc_nn)
            if not apply_rule:
                df_words = [df[word] for word in doc[0]]
                idx = heapq.nlargest(1, xrange(len(df_words)), key=df_words.__getitem__)
                corpus_keyword.append([doc[0][ith] for ith in idx])
        else:
            corpus_keyword.append(doc[0])
    return corpus_keyword

def main_category_clustering(df, corpus, corpus_keyword, original_sent):
    # Freq threshold is determined by insuring 70% of sentences is clustered
    df_ordered = df.most_common()
    sent_count = 0
    for word in df_ordered:
        sent_count += word[1]
        if sent_count >= 0.7*len(corpus):
            freq_threshold = word[1]-1
            break
    print 'Freq threshold:', freq_threshold

    major_list = [word[0] for word in df_ordered if word[1] > freq_threshold]
    print "major category:\n", major_list

    cluster_info = []  # format: [[label, freq, centroid_sentence],...]

    clustered_index = []
    for word in major_list:
        idx_set = []
        for idx, doc in enumerate(corpus_keyword):
            if word in doc:
                idx_set.append(idx)
                corpus[idx] = corpus[idx] + (word,)
        clustered_index = clustered_index + idx_set

        cluster_doc = [original_sent[i][0] for i in idx_set]
        cluster_centroid = get_Cluster_Centroid(cluster_doc)
        # centroid_sentence_idx = idx_set[cluster_centroid]
        cluster_info.append([word, len(idx_set), cluster_centroid])

    clustered_index = set(clustered_index)
    unclustered_index = list(set(range(len(corpus))) - clustered_index)
    print "No. of clustered sentences:", len(clustered_index)
    print "No. of unclustered sentences:", len(unclustered_index)
    for idx in unclustered_index:
        corpus[idx] = corpus[idx] + ("others",)

    return corpus, cluster_info


def filter_rule_q1(doc, xth, corpus_keyword, original_corpus):
    apply_rule = False
    # rules (priority from high to low)
    if 'app' in doc:
        corpus_keyword.append(['app'])
        apply_rule = True
        return apply_rule
    elif 'without_appointment' in doc:
        corpus_keyword.append(['without_appointment'])
        apply_rule = True
        return apply_rule
    elif 'sm' in doc:
        corpus_keyword.append(['sm'])
        apply_rule = True
        return apply_rule
    elif 'onlin' in doc:
        corpus_keyword.append(['onlin'])
        apply_rule = True
        return apply_rule
    elif 'emerg' in doc:
        corpus_keyword.append(['emerg'])
        apply_rule = True
        return apply_rule
    elif 'deliv' in doc:
        corpus_keyword.append(['deliv'])
        apply_rule = True
        return apply_rule
    elif 'inform' in doc:
        corpus_keyword.append(['inform'])
        apply_rule = True
        return apply_rule
    elif 'fix' in doc:
        corpus_keyword.append(['fix'])
        apply_rule = True
        return apply_rule
    elif 'pick' in doc and 'drop' in doc:
        corpus_keyword.append(['pick'])
        apply_rule = True
        return apply_rule
    elif 'wait' in doc and 'month' not in original_corpus[xth][0]:
        corpus_keyword.append(['wait'])
        apply_rule = True
        return apply_rule
    elif 'hour' in doc:
        corpus_keyword.append(['wait'])
        apply_rule = True
        return apply_rule
    elif 'appointment' in doc or 'day' in doc or 'week' in doc and 'call' in doc:  # from call to appointment
        corpus_keyword.append(['appointment'])
        apply_rule = True
        return apply_rule
    else:
        return apply_rule


def filter_rule_q2(doc, xth, corpus, original_corpus):
    apply_rule = False
    # rules (priority from high to low)
    return apply_rule

def filter_rule_q3(doc, xth, corpus, original_corpus):
    apply_rule = False
    # rules (priority from high to low)
    return apply_rule

def filter_rule_q4(doc, xth, corpus, original_corpus):
    apply_rule = False
    # rules (priority from high to low)
    return apply_rule

def filter_rule_q5(doc, xth, corpus, original_corpus):
    apply_rule = False
    # rules (priority from high to low)
    return apply_rule

def filter_rule_q6(doc, xth, corpus, original_corpus):
    apply_rule = False
    # rules (priority from high to low)
    return apply_rule

def filter_rule_q7(doc, xth, corpus, original_corpus):
    apply_rule = False
    # rules (priority from high to low)
    return apply_rule

def filter_rule_q8(doc, xth, corpus, original_corpus):
    apply_rule = False
    # rules (priority from high to low)
    return apply_rule

def filter_rule_q9(doc, xth, corpus, original_corpus):
    apply_rule = False
    # rules (priority from high to low)
    return apply_rule

def filter_rule_q10(doc, xth, corpus, original_corpus):
    apply_rule = False
    # rules (priority from high to low)
    return apply_rule