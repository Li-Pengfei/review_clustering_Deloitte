import numpy as np
from gensim import corpora
from gensim.models import TfidfModel
from gensim.models import LsiModel
from gensim.similarities import MatrixSimilarity
from gensim.matutils import corpus2dense
from sklearn.metrics.pairwise import cosine_similarity

def get_Cluster_Centroid(corpus):
    # given a set of documents, return the index of the document centroid
    dictionary = corpora.Dictionary(corpus)
    corpus_gensim = [dictionary.doc2bow(doc) for doc in corpus]
    tfidf = TfidfModel(corpus_gensim)
    corpus_tfidf = tfidf[corpus_gensim]

    lsi = LsiModel(corpus_tfidf, id2word=dictionary, num_topics=50)
    lsi_proj = lsi[corpus_tfidf]
    numpy_matrix = corpus2dense(lsi_proj, num_terms=50, num_docs=len(corpus)).T

    centroid_vec = 0
    for vec in numpy_matrix:
        centroid_vec += vec
    centroid_vec = centroid_vec/len(corpus)

    sim_list = cosine_similarity(centroid_vec.reshape(1, -1),numpy_matrix )[0]
    sim_ordered = sorted(enumerate(sim_list), key=lambda item: -item[1])
    return sim_ordered[0][0]

