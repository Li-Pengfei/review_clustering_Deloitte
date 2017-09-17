import survey_reader
import pre_processing
import post_processing
import rule_based_clustering
import auto_clustering
from q2_timeinfo import time_extract, day_extract
import pandas as pd


label = pd.Series()


def process_question(ques_num, csv_path):
    assert (ques_num in range(1, 11)), "Question number must between 1-10 (inclusive)!"

    file = survey_reader.read_Surveycsv(csv_path)
    content = file[ques_num][0]
    index = file[ques_num][1]
    print 'Length of content', len(content)

    switcher = {
        1: q1, 2: q2, 3:q3
    }
    # Get the function from switcher dictionary to process corresponding question
    func = switcher.get(ques_num)
    # Execute the function
    return func(content, csv_path)

def q1(content, csv_path):
    return

def q3(content, csv_path):
    pos_tags = ['NN', 'NNS', 'JJ', 'JJR', 'JJS']
    doc_noimprove, doc_extracted, doc_other = pre_processing.process_corpus(content, pos_tags, question=3)
    doc_nn, nn_extracted = doc_extracted[0], doc_extracted[1]
    print 'Comment with keywords:', len(doc_nn)
    print 'No comments:', len(doc_noimprove)
    print 'Comment without keywords:', len(doc_other)

    # df = post_processing.df_count(nn_extracted)
    # print df

    # Rule-based clustering
    unclustered_index, nn_extracted = rule_based_clustering.clustering(nn_extracted, question=3)

    # LSI + Spectral Clustering
    nn_extracted_unclustered = [nn_extracted[i][0] for i in unclustered_index]
    similarity_matrix = auto_clustering.lsi(nn_extracted_unclustered)
    label_auto = auto_clustering.spectral_clustering(similarity_matrix, nn_extracted_unclustered)
    for i, idx in enumerate(unclustered_index):
        nn_extracted[idx] = nn_extracted[idx] + (label_auto[i],)

    return nn_extracted






def q2(content, csv_path):
    pos_tags = []
    doc_noimprove, doc_extracted, doc_other = pre_processing.process_corpus(content, pos_tags, question=2)
    doc_day, doc_time = doc_extracted[0], doc_extracted[1]
    for idx, sing_review in enumerate(doc_day):
        doc_day[idx] = (sing_review[0], sing_review[1], day_extract(sing_review))
    for idx, sing_review in enumerate(doc_time):
        doc_time[idx] = (sing_review[0], sing_review[1], time_extract(sing_review))
    for idx, sing_review in enumerate(doc_noimprove):
        doc_noimprove[idx] = (sing_review[0], sing_review[1], 'noimprove')
    for idx, sing_review in enumerate(doc_other):
        doc_other[idx] = (sing_review[0], sing_review[1], 'others')
    return doc_day + doc_time + doc_noimprove + doc_other




if __name__ == '__main__':

    process_question(2, '../raw_data/survey_data.csv')




