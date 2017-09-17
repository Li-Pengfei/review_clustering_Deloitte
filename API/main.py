import survey_reader
import pre_processing
import post_processing
import rule_based_clustering
import auto_clustering

import pandas as pd


label = pd.Series()


def process_question(ques_num, csv_path):
    file = survey_reader.read_Surveycsv(csv_path)
    content = file[ques_num][0]
    index = file[ques_num][1]

    print 'Length of content', len(content)

    switcher = {
        1: q1, 2: q2
    }
    # Get the function from switcher dictionary to process corresponding question
    func = switcher.get(ques_num, lambda: "Question number must between 1-10 (inclusive)!")
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

    df = post_processing.df_count(nn_extracted)
    # print df

    # Rule-based clustering
    unclustered_index, nn_extracted = rule_based_clustering.clustering(nn_extracted, question=3)

    # LSI + Spectral Clustering
    nn_extracted_unclustered = [nn_extracted[i][0] for i in unclustered_index]
    similarity_matrix = auto_clustering.lsi(nn_extracted_unclustered)
    auto_clustering.spectral_clustering(similarity_matrix, nn_extracted_unclustered)






def q2(content, csv_path):
    pos_tags = []
    doc_noimprove, doc_extracted, doc_other = pre_processing.process_corpus(content, pos_tags, question=2)
    doc_day, doc_time = doc_extracted[0], doc_extracted[1]
    print doc_time




if __name__ == '__main__':

    process_question(2, '../raw_data/survey_data.csv')




