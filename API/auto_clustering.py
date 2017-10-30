import post_processing
from string import join
import numpy as np
from gensim import corpora
from gensim.models import TfidfModel
from gensim.models import LsiModel
from gensim.similarities import MatrixSimilarity
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import SpectralClustering
from cluster_centroid import get_Cluster_Centroid

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

def spectral_clustering(similarity_matrix, corpus):
    n_clusters_ = 5
    sc = SpectralClustering(n_clusters=n_clusters_, affinity='precomputed').fit(similarity_matrix)
    labels = sc.labels_
    word_labels = ['']*len(labels)
    print('Estimated number of clusters: %d' % n_clusters_)

    cluster_info = []  # format: [[label, freq, centroid_sentence_idx],...]

    for indice_cluster in range(n_clusters_):
        idx_list = np.where(labels == indice_cluster)[0]

        cluster_corpus = [sentence for idx, sentence in enumerate(corpus) if idx in idx_list]

        df = post_processing.df_count(cluster_corpus)
        label = df.most_common(3)[0][0]
        label2 = df.most_common(3)[1][0]
        label3 = df.most_common(3)[2][0]
        cluster_label = "_".join([label, label2, label3])

        for idx in idx_list:
            word_labels[idx] = cluster_label

        cluster_centroid = get_Cluster_Centroid(cluster_corpus)
        centroid_sentence_idx = idx_list[cluster_centroid]
        cluster_info.append([cluster_label, len(idx_list), centroid_sentence_idx])
    print("The remaining sentences are automatically clustered")
    return word_labels, cluster_info






