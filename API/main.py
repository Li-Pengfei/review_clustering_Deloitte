import survey_reader
import pre_processing
import post_processing
import rule_based_clustering
import auto_clustering
from q2_timeinfo import time_extract, day_extract
import pandas as pd
import survey_writer
import numpy as np


label = pd.Series()

from survey_writer import write_Label

label = pd.Series()


def process_question(ques_num, input_path, cluster_info_path):
    assert (ques_num in range(1, 11)), "Question number must between 1-10 (inclusive)!"

    file = survey_reader.read_Surveycsv(input_path)
    content = file[ques_num][0]
    index = file[ques_num][1]
    print 'Number of content', len(content)

    switcher = {
        1:q1, 2:q2, 3:q3, 4:q4, 5:q5, 6:q6, 7:q7, 8:q8, 9:q9, 10:q10
    }
    # Get the function from switcher dictionary to process corresponding question
    func = switcher.get(ques_num)
    # Execute the function
    result_cluster, cluster_info_all = func(content)
    # print result_cluster
    # print cluster_info_all
    survey_writer.write_Label(content, result_cluster, input_path, index)
    survey_writer.write_Cluster_Info(cluster_info_all, cluster_info_path)



def q1(content):
    pos_tags = ['NN', 'NNS', 'JJ', 'JJR', 'JJS']
    doc_noimprove, doc_extracted, doc_other = pre_processing.process_corpus(content, pos_tags, question=1)
    doc_nn, nn_extracted = doc_extracted[0], doc_extracted[1]
    print 'Comment with keywords:', len(doc_nn)
    print 'No comments:', len(doc_noimprove)
    print 'Comment without keywords:', len(doc_other), "\n"
    df = post_processing.df_count_tuple(nn_extracted)
    # print df

    # extract one most representative keyword for each sentence
    nn_clean = post_processing.filter_ne(nn_extracted, doc_nn, df, question=1)
    df = post_processing.df_count(nn_clean)
    nn_extracted, cluster_info = post_processing.main_category_clustering(df, nn_extracted, nn_clean)

    # cluster_info_all format: [[question number, label, freq, centroid_sentence],...]
    cluster_info_all = [[1, info[0], info[1], doc_nn[info[2]][0]] for info in cluster_info]

    return nn_extracted + doc_noimprove + doc_other, cluster_info_all



def q2(content):
    pos_tags = []
    doc_noimprove, doc_extracted, doc_other = pre_processing.process_corpus(content, pos_tags, question=2)
    doc_day, doc_time = doc_extracted[0], doc_extracted[1]
    label_day = []
    label_time = []
    cluster_info_all=[]

    for idx, sing_review in enumerate(doc_day):
        doc_day[idx] = (sing_review[0], sing_review[1], day_extract(sing_review))
        label_day.append(day_extract(sing_review))
    for idx, sing_review in enumerate(doc_time):
        doc_time[idx] = (sing_review[0], sing_review[1], time_extract(sing_review))
        label_time.append(time_extract(sing_review))

    unique_day, unique_day_indices = np.unique(label_day, return_inverse=True)
    for i in range(len(unique_day)):
        label = unique_day[i]
        idx_set = np.where(np.array(unique_day_indices) == i)[0]
        sent = doc_day[idx_set[0]][0]
        cluster_info_all.append([2, label, len(idx_set), sent])

    cluster_info_all.append([2, 'specific_time', len(doc_time), ''])

    return doc_day + doc_time + doc_noimprove + doc_other, cluster_info_all

def q3(content):
    pos_tags = ['NN', 'NNS', 'JJ', 'JJR', 'JJS']
    doc_noimprove, doc_extracted, doc_other = pre_processing.process_corpus(content, pos_tags, question=3)
    doc_nn, nn_extracted = doc_extracted[0], doc_extracted[1]
    print 'Comment with keywords:', len(doc_nn)
    print 'No comments:', len(doc_noimprove)
    print 'Comment without keywords:', len(doc_other), "\n"

    # Rule-based clustering
    unclustered_index, nn_extracted, cluster_info = rule_based_clustering.clustering(nn_extracted, question=3)

    # cluster_info_all format: [[question number, label, freq, centroid_sentence],...]
    cluster_info_all = [[3, info[0], info[1], doc_nn[info[2]][0]] for info in cluster_info]

    # LSI + Spectral Clustering
    nn_extracted_unclustered = [nn_extracted[i][0] for i in unclustered_index]
    doc_nn_unclustered = [doc_nn[i] for i in unclustered_index]
    similarity_matrix = auto_clustering.lsi(nn_extracted_unclustered)
    label_auto, cluster_info = auto_clustering.spectral_clustering(similarity_matrix, nn_extracted_unclustered)
    for i, idx in enumerate(unclustered_index):
        nn_extracted[idx] = nn_extracted[idx] + (label_auto[i],)

    for info in cluster_info:
        cluster_info_all.append([3, info[0], info[1], doc_nn_unclustered[info[2]][0]])

    return nn_extracted + doc_noimprove + doc_other, cluster_info_all

def q4(content):
    pos_tags = ['NN', 'NNS']
    doc_noimprove, doc_extracted, doc_other = pre_processing.process_corpus(content, pos_tags, question=4)
    doc_nn, nn_extracted = doc_extracted[0], doc_extracted[1]
    print 'Comment with keywords:', len(doc_nn)
    print 'No comments:', len(doc_noimprove)
    print 'Comment without keywords:', len(doc_other)
    df = post_processing.df_count_tuple(nn_extracted)

    nn_clean = post_processing.filter_ne(nn_extracted, doc_nn, df, question=4)
    df = post_processing.df_count(nn_clean)
    nn_extracted, cluster_info = post_processing.main_category_clustering(df, nn_extracted, nn_clean)

    # cluster_info_all format: [[question number, label, freq, centroid_sentence],...]
    cluster_info_all = [[4, info[0], info[1], doc_nn[info[2]][0]] for info in cluster_info]

    return nn_extracted + doc_noimprove + doc_other, cluster_info_all


def q5(content):
    pos_tags = ['NN', 'NNS', 'JJ', 'JJR', 'JJS']
    doc_noimprove, doc_extracted, doc_other = pre_processing.process_corpus(content, pos_tags, question=5)
    doc_nn, nn_extracted = doc_extracted[0], doc_extracted[1]
    print 'Comment with keywords:', len(doc_nn)
    print 'No comments:', len(doc_noimprove)
    print 'Comment without keywords:', len(doc_other), "\n"


    # LSI + Spectral Clustering
    nn_extracted_corpus = [nn_single[0] for nn_single in nn_extracted]
    similarity_matrix = auto_clustering.lsi(nn_extracted_corpus)
    label_auto, cluster_info = auto_clustering.spectral_clustering(similarity_matrix, nn_extracted_corpus, cluster_num=10)
    for idx in range(len(nn_extracted_corpus)):
        nn_extracted[idx] = nn_extracted[idx] + (label_auto[idx],)
    # for idx in range(len(doc_noimprove)):
    #     doc_noimprove[idx] = doc_noimprove[idx] + ('noimprove', )
    # for idx in range(len(doc_other)):
    #     doc_other[idx] = doc_other[idx] + ('others', )

    cluster_info_all = [[5, info[0], info[1], doc_nn[info[2]][0]] for info in cluster_info]
    return nn_extracted + doc_noimprove + doc_other, cluster_info_all

def q6(content):
    pos_tags = ['NN', 'NNS']
    doc_noimprove, doc_extracted, doc_other = pre_processing.process_corpus(content, pos_tags, question=6)
    doc_nn, nn_extracted = doc_extracted[0], doc_extracted[1]
    print 'Comment with keywords:', len(doc_nn)
    print 'No comments:', len(doc_noimprove)
    print 'Comment without keywords:', len(doc_other), "\n"

    # Rule-based clustering
    unclustered_index, nn_extracted, cluster_info = rule_based_clustering.clustering(nn_extracted, question=6)

    # cluster_info_all format: [[question number, label, freq, centroid_sentence],...]
    cluster_info_all = [[6, info[0], info[1], doc_nn[info[2]][0]] for info in cluster_info]

    # LSI + Spectral Clustering
    nn_extracted_unclustered = [nn_extracted[i][0] for i in unclustered_index]
    doc_nn_unclustered = [doc_nn[i] for i in unclustered_index]
    similarity_matrix = auto_clustering.lsi(nn_extracted_unclustered)
    label_auto, cluster_info = auto_clustering.spectral_clustering(similarity_matrix, nn_extracted_unclustered)
    for i, idx in enumerate(unclustered_index):
        nn_extracted[idx] = nn_extracted[idx] + (label_auto[i],)

    for info in cluster_info:
        cluster_info_all.append([6, info[0], info[1], doc_nn_unclustered[info[2]][0]])

    return nn_extracted + doc_noimprove + doc_other, cluster_info_all

def q7(content):
    pos_tags = ['NN', 'NNS']
    doc_noimprove, doc_extracted, doc_other = pre_processing.process_corpus(content, pos_tags, question=7)
    doc_nn, nn_extracted = doc_extracted[0], doc_extracted[1]
    print 'Comment with keywords:', len(doc_nn)
    print 'No comments:', len(doc_noimprove)
    print 'Comment without keywords:', len(doc_other), "\n"
    df = post_processing.df_count_tuple(nn_extracted)

    nn_clean = post_processing.filter_ne(nn_extracted, doc_nn, df, question=7)
    df = post_processing.df_count(nn_clean)
    nn_extracted, cluster_info = post_processing.main_category_clustering(df, nn_extracted, nn_clean)

    # cluster_info_all format: [[question number, label, freq, centroid_sentence],...]
    cluster_info_all = [[7, info[0], info[1], doc_nn[info[2]][0]] for info in cluster_info]

    return nn_extracted + doc_noimprove + doc_other, cluster_info_all

def q8(content):
    pos_tags = ['NN', 'NNS']
    doc_noimprove, doc_extracted, doc_other = pre_processing.process_corpus(content, pos_tags, question=8)
    doc_nn, nn_extracted = doc_extracted[0], doc_extracted[1]
    print 'Comment with keywords:', len(doc_nn)
    print 'No comments:', len(doc_noimprove)
    print 'Comment without keywords:', len(doc_other), "\n"
    df = post_processing.df_count_tuple(nn_extracted)

    # extract one most representative keyword for each sentence
    nn_clean = post_processing.filter_ne(nn_extracted, doc_nn, df, question=8)
    df = post_processing.df_count(nn_clean)
    nn_extracted, cluster_info = post_processing.main_category_clustering(df, nn_extracted, nn_clean)

    # cluster_info_all format: [[question number, label, freq, centroid_sentence],...]
    cluster_info_all = [[8, info[0], info[1], doc_nn[info[2]][0]] for info in cluster_info]

    return nn_extracted + doc_noimprove + doc_other, cluster_info_all

def q9(content):
    pos_tags = ['NN', 'NNS']
    doc_noimprove, doc_extracted, doc_other = pre_processing.process_corpus(content, pos_tags, question=9)
    doc_nn, nn_extracted = doc_extracted[0], doc_extracted[1]
    print 'Comment with keywords:', len(doc_nn)
    print 'No comments:', len(doc_noimprove)
    print 'Comment without keywords:', len(doc_other)
    df = post_processing.df_count_tuple(nn_extracted)

    nn_clean = post_processing.filter_ne(nn_extracted, doc_nn, df, question=9)
    df = post_processing.df_count(nn_clean)
    nn_extracted, cluster_info = post_processing.main_category_clustering(df, nn_extracted, nn_clean)

    # cluster_info_all format: [[question number, label, freq, centroid_sentence],...]
    cluster_info_all = [[9, info[0], info[1], doc_nn[info[2]][0]] for info in cluster_info]

    return nn_extracted + doc_noimprove + doc_other, cluster_info_all


def q10(content):
    pos_tags = ['NN', 'NNS', 'JJ', 'JJR', 'JJS']
    doc_noimprove, doc_extracted, doc_other = pre_processing.process_corpus(content, pos_tags, question=10)
    doc_nn, nn_extracted = doc_extracted[0], doc_extracted[1]
    print 'Comment with keywords:', len(doc_nn)
    print 'No comments:', len(doc_noimprove)
    print 'Comment without keywords:', len(doc_other), "\n"


    # LSI + Spectral Clustering
    nn_extracted_corpus = [nn_single[0] for nn_single in nn_extracted]
    similarity_matrix = auto_clustering.lsi(nn_extracted_corpus)
    label_auto, cluster_info = auto_clustering.spectral_clustering(similarity_matrix, nn_extracted_corpus, cluster_num=10)
    for idx in range(len(nn_extracted_corpus)):
        nn_extracted[idx] = nn_extracted[idx] + (label_auto[idx],)
    # for idx in range(len(doc_noimprove)):
    #     doc_noimprove[idx] = doc_noimprove[idx] + ('noimprove', )
    # for idx in range(len(doc_other)):
    #     doc_other[idx] = doc_other[idx] + ('others', )

    cluster_info_all = [[10, info[0], info[1], doc_nn[info[2]][0]] for info in cluster_info]

    return nn_extracted + doc_noimprove + doc_other, cluster_info_all

    
if __name__ == '__main__':

    process_question(2, '../raw_data/survey_data.csv','../raw_data/survey_cluster.csv')




