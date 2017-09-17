from collections import Counter

def df_count(corpus):
    text = []
    for comment in corpus:
        text = text + comment[0]
    df = Counter(text)
    return df

def filter_ne(corpus, df):  # assuming each review contain one aspect
    for xth, doc in enumerate(test_corpus):
        if len(doc)>1:
            df_words = [df[word] for word in doc]
            idx =  heapq.nlargest(1, xrange(len(df_words)), key=df_words.__getitem__)
            test_corpus[xth] = [stemmer.stem(doc[ith]) for ith in idx]
    return test_corpus

def main_category(df_map, nn_clean, corpus): # new main_cate func. with common index
    if (not os.path.isdir("cluster")):
        os.mkdir("cluster")
    name_list = {}
    major_list = [word for word in df_list if df_list[word]/len(dict_map)>0.05]
    print "majot list:\n", major_list
    for word in major_list:
        if not os.path.isdir("cluster/%s" %word):
            os.mkdir("cluster/%s" %word)
        idx_set = []
        for idx, doc in enumerate(nn_clean):
            if word in doc:
                idx_set.append(idx)
        write_file(doc_nn, idx_set, word)
        name_list[word] = idx_set
    return name_list, len(set(scidx_set))