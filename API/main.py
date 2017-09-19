import survey_reader
import pre_processing
import post_processing
import rule_based_clustering
import auto_clustering
from q2_timeinfo import time_extract, day_extract
import pandas as pd
from survey_writer import write_Surveycsv


label = pd.Series()

from survey_writer import write_Surveycsv

label = pd.Series()


def process_question(ques_num, input_path, output_path):
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
    result_cluster = func(content, input_path)
    # print result_cluster
    write_Surveycsv(content, result_cluster, output_path+'/%d_tmp.csv' %ques_num)



def q1(content, csv_path):
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
    nn_extracted = post_processing.main_category_clustering(df, nn_extracted, nn_clean)

    return nn_extracted + doc_noimprove + doc_other



def q2(content, csv_path):
    pos_tags = []
    doc_noimprove, doc_extracted, doc_other = pre_processing.process_corpus(content, pos_tags, question=2)
    doc_day, doc_time = doc_extracted[0], doc_extracted[1]
    for idx, sing_review in enumerate(doc_day):
        doc_day[idx] = (sing_review[0], sing_review[1], day_extract(sing_review))
    for idx, sing_review in enumerate(doc_time):
        doc_time[idx] = (sing_review[0], sing_review[1], time_extract(sing_review))
    # for idx, sing_review in enumerate(doc_noimprove):
    #     doc_noimprove[idx] = (sing_review[0], sing_review[1], 'noimprove')
    # for idx, sing_review in enumerate(doc_other):
    #     doc_other[idx] = (sing_review[0], sing_review[1], 'others')
    return doc_day + doc_time + doc_noimprove + doc_other

def q3(content, csv_path):
    pos_tags = ['NN', 'NNS', 'JJ', 'JJR', 'JJS']
    doc_noimprove, doc_extracted, doc_other = pre_processing.process_corpus(content, pos_tags, question=3)
    doc_nn, nn_extracted = doc_extracted[0], doc_extracted[1]
    print 'Comment with keywords:', len(doc_nn)
    print 'No comments:', len(doc_noimprove)
    print 'Comment without keywords:', len(doc_other), "\n"

    # Rule-based clustering
    unclustered_index, nn_extracted = rule_based_clustering.clustering(nn_extracted, question=3)

    # LSI + Spectral Clustering
    nn_extracted_unclustered = [nn_extracted[i][0] for i in unclustered_index]
    similarity_matrix = auto_clustering.lsi(nn_extracted_unclustered)
    label_auto = auto_clustering.spectral_clustering(similarity_matrix, nn_extracted_unclustered)
    for i, idx in enumerate(unclustered_index):
        nn_extracted[idx] = nn_extracted[idx] + (label_auto[i],)

    return nn_extracted + doc_noimprove + doc_other

def q4(content, csv_path):
    pos_tags = ['NN', 'NNS']
    doc_noimprove, doc_extracted, doc_other = pre_processing.process_corpus(content, pos_tags, question=4)
    doc_nn, nn_extracted = doc_extracted[0], doc_extracted[1]
    print 'Comment with keywords:', len(doc_nn)
    print 'No comments:', len(doc_noimprove)
    print 'Comment without keywords:', len(doc_other)
    df = post_processing.df_count_tuple(nn_extracted)

    nn_clean = post_processing.filter_ne(nn_extracted, doc_nn, df, question=4)
    df = post_processing.df_count(nn_clean)
    nn_extracted = post_processing.main_category_clustering(df, nn_extracted, nn_clean)

    return nn_extracted + doc_noimprove + doc_other


def q5(content, csv_path):
    pos_tags = ['NN', 'NNS', 'JJ', 'JJR', 'JJS']
    doc_noimprove, doc_extracted, doc_other = pre_processing.process_corpus(content, pos_tags, question=5)
    doc_nn, nn_extracted = doc_extracted[0], doc_extracted[1]
    print 'Comment with keywords:', len(doc_nn)
    print 'No comments:', len(doc_noimprove)
    print 'Comment without keywords:', len(doc_other), "\n"


    # LSI + Spectral Clustering
    nn_extracted_corpus = [nn_single[0] for nn_single in nn_extracted]
    similarity_matrix = auto_clustering.lsi(nn_extracted_corpus)
    label_auto = auto_clustering.spectral_clustering(similarity_matrix, nn_extracted_corpus)
    for idx in range(len(nn_extracted_corpus)):
        nn_extracted[idx] = nn_extracted[idx] + (label_auto[idx],)
    # for idx in range(len(doc_noimprove)):
    #     doc_noimprove[idx] = doc_noimprove[idx] + ('noimprove', )
    # for idx in range(len(doc_other)):
    #     doc_other[idx] = doc_other[idx] + ('others', )
    return nn_extracted + doc_noimprove + doc_other

def q6(content, csv_path):
    pos_tags = ['NN', 'NNS']
    doc_noimprove, doc_extracted, doc_other = pre_processing.process_corpus(content, pos_tags, question=6)
    doc_nn, nn_extracted = doc_extracted[0], doc_extracted[1]
    print 'Comment with keywords:', len(doc_nn)
    print 'No comments:', len(doc_noimprove)
    print 'Comment without keywords:', len(doc_other), "\n"

    # Rule-based clustering
    unclustered_index, nn_extracted = rule_based_clustering.clustering(nn_extracted, question=6)

    # LSI + Spectral Clustering
    nn_extracted_unclustered = [nn_extracted[i][0] for i in unclustered_index]
    similarity_matrix = auto_clustering.lsi(nn_extracted_unclustered)
    label_auto = auto_clustering.spectral_clustering(similarity_matrix, nn_extracted_unclustered)
    for i, idx in enumerate(unclustered_index):
        nn_extracted[idx] = nn_extracted[idx] + (label_auto[i],)

    return nn_extracted + doc_noimprove + doc_other

def q7(content, csv_path):
    pos_tags = ['NN', 'NNS']
    doc_noimprove, doc_extracted, doc_other = pre_processing.process_corpus(content, pos_tags, question=7)
    doc_nn, nn_extracted = doc_extracted[0], doc_extracted[1]
    print 'Comment with keywords:', len(doc_nn)
    print 'No comments:', len(doc_noimprove)
    print 'Comment without keywords:', len(doc_other), "\n"
    df = post_processing.df_count_tuple(nn_extracted)

    nn_clean = post_processing.filter_ne(nn_extracted, doc_nn, df, question=7)
    df = post_processing.df_count(nn_clean)
    nn_extracted = post_processing.main_category_clustering(df, nn_extracted, nn_clean)

    return nn_extracted + doc_noimprove + doc_other

def q8(content, csv_path):
    pos_tags = ['NN', 'NNS']
    doc_noimprove, doc_extracted, doc_other = pre_processing.process_corpus(content, pos_tags, question=8)
    doc_nn, nn_extracted = doc_extracted[0], doc_extracted[1]
    print 'Comment with keywords:', len(doc_nn)
    print 'No comments:', len(doc_noimprove)
    print 'Comment without keywords:', len(doc_other), "\n"
    df = post_processing.df_count_tuple(nn_extracted)
    # print df

    # extract one most representative keyword for each sentence
    nn_clean = post_processing.filter_ne(nn_extracted, doc_nn, df, question=8)
    df = post_processing.df_count(nn_clean)
    nn_extracted = post_processing.main_category_clustering(df, nn_extracted, nn_clean)

    return nn_extracted + doc_noimprove + doc_other

def q9(content, csv_path):
    pos_tags = ['NN', 'NNS']
    doc_noimprove, doc_extracted, doc_other = pre_processing.process_corpus(content, pos_tags, question=9)
    doc_nn, nn_extracted = doc_extracted[0], doc_extracted[1]
    print 'Comment with keywords:', len(doc_nn)
    print 'No comments:', len(doc_noimprove)
    print 'Comment without keywords:', len(doc_other)
    df = post_processing.df_count_tuple(nn_extracted)

    nn_clean = post_processing.filter_ne(nn_extracted, doc_nn, df, question=9)
    df = post_processing.df_count(nn_clean)
    nn_extracted = post_processing.main_category_clustering(df, nn_extracted, nn_clean)

    return nn_extracted + doc_noimprove + doc_other


def q10(content, csv_path):
    pos_tags = ['NN', 'NNS', 'JJ', 'JJR', 'JJS']
    doc_noimprove, doc_extracted, doc_other = pre_processing.process_corpus(content, pos_tags, question=10)
    doc_nn, nn_extracted = doc_extracted[0], doc_extracted[1]
    print 'Comment with keywords:', len(doc_nn)
    print 'No comments:', len(doc_noimprove)
    print 'Comment without keywords:', len(doc_other), "\n"


    # LSI + Spectral Clustering
    nn_extracted_corpus = [nn_single[0] for nn_single in nn_extracted]
    similarity_matrix = auto_clustering.lsi(nn_extracted_corpus)
    label_auto = auto_clustering.spectral_clustering(similarity_matrix, nn_extracted_corpus)
    for idx in range(len(nn_extracted_corpus)):
        nn_extracted[idx] = nn_extracted[idx] + (label_auto[idx],)
    # for idx in range(len(doc_noimprove)):
    #     doc_noimprove[idx] = doc_noimprove[idx] + ('noimprove', )
    # for idx in range(len(doc_other)):
    #     doc_other[idx] = doc_other[idx] + ('others', )
    return nn_extracted + doc_noimprove + doc_other

    
if __name__ == '__main__':

    process_question(10, '../raw_data/survey_data.csv')




