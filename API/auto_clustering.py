import numpy as np
from gensim import corpora
from gensim.models import TfidfModel
from gensim.models import LsiModel
from gensim.similarities import MatrixSimilarity
from sklearn.metrics.pairwise import cosine_similarity

def lsi(corpus):
    dictionary = corpora.Dictionary(corpus)
    corpus_gensim = [dictionary.doc2bow(doc) for doc in corpus]
    tfidf = TfidfModel(corpus_gensim)
    corpus_tfidf = tfidf[corpus_gensim]

    lsi = LsiModel(corpus_tfidf, id2word=dictionary, num_topics=50)
    lsi_proj = lsi[corpus_tfidf]

    lsi_index = MatrixSimilarity(lsi_proj)
    similarity_matrix = np.array([lsi_index[lsi[corpus_tfidf[i]]] for i in range(len(corpus))])

    # convert similarity_matrix from -1~1 to 0~1
    def f(x):
        return (x + 1) / 2
    f = np.vectorize(f, otypes=[np.float])
    similarity_matrix = f(similarity_matrix)
    return similarity_matrix

def spectral_clustering():

