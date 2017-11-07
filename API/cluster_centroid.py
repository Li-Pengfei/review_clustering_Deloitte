import numpy as np
from gensim import corpora
from gensim.models import TfidfModel
from gensim.models import LsiModel
from gensim.similarities import MatrixSimilarity
from gensim.matutils import corpus2dense
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.stem.porter import PorterStemmer
from pre_processing import global_remove_list


stemmer = PorterStemmer()
stop_words = stopwords.words('english')

def get_Cluster_Centroid(corpus):
    # given a set of documents, return the document centroid sentence on the tf-idf vector space

    sentence = []
    sent_tokens = []
    min_sent_len = 100
    max_sent_len = 0
    for comment in corpus:
        sents = sent_tokenize(comment)    # split comment into single sentence
        for sent in sents:
            sentence.append(sent)
            # find min and max sentence length
            sent_len = len(word_tokenize(sent))
            if sent_len < min_sent_len:
                min_sent_len = sent_len
            if sent_len > max_sent_len:
                max_sent_len = sent_len
            # tokenize and remove stopwords
            tokens = [token for token in word_tokenize(sent) if token not in stop_words]
            # stemming and remove common words
            sent_tokens.append([stemmer.stem(word) for word in tokens if stemmer.stem(word) not in global_remove_list])

    dictionary = corpora.Dictionary(sent_tokens)
    corpus_gensim = [dictionary.doc2bow(doc) for doc in sent_tokens]
    tfidf = TfidfModel(corpus_gensim)
    corpus_tfidf = tfidf[corpus_gensim]

    lsi = LsiModel(corpus_tfidf, id2word=dictionary, num_topics=50)
    lsi_proj = lsi[corpus_tfidf]
    numpy_matrix = corpus2dense(lsi_proj, num_terms=50, num_docs=len(sent_tokens)).T

    centroid_vec = 0
    for vec in numpy_matrix:
        centroid_vec += vec
    centroid_vec = centroid_vec/len(sent_tokens)

    sim_list = cosine_similarity(centroid_vec.reshape(1, -1),numpy_matrix )[0]
    sim_ordered = sorted(enumerate(sim_list), key=lambda item: -item[1])

    # find the sentence closest to centroid and length smaller than max_sent_len
    sent_len_threshold = min_sent_len + (max_sent_len-min_sent_len)/4
    # print "threshold", sent_len_threshold
    centroid_sent = sentence[sim_ordered[0][0]]
    for index in sim_ordered:
        sent_len = len(word_tokenize(sentence[index[0]]))
        if 5 < sent_len < sent_len_threshold:
            centroid_sent = sentence[index[0]]
            break
    return centroid_sent

