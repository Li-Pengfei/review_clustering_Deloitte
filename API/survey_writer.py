import string
import numpy as np
import pandas as pd
import nltk
import cPickle
import data_helper
# from keras.preprocessing import sequence
from sklearn import preprocessing

def rule_q2(tt_list):
    tt_list = ['others' if x == (None, None) else x for x in tt_list]
    tt_list = list(set(tt_list))
    if len(tt_list)>1 and 'others' in tt_list:
        tt_list.remove('others')
    return tt_list


def write_Surveycsv(content, listuple, csv_path):
    ##creating pandas
    idx_comment = range(len(content))
    df_comment = pd.DataFrame({'id': idx_comment, 'comment': content})
    df_survey = pd.DataFrame(listuple, columns=['sentence', 'id', 'label'])
    df_all = pd.merge(df_comment, df_survey, on='id', how='inner')
    df_final = df_all.groupby(['id', 'comment'])['label'].apply(list).to_frame()

    df_final['label'] = df_final['label'].apply(lambda x: rule_q2(x))
    df_final.to_csv(csv_path)
    ###

def fileWriter(filename, file):
    """
    author: Pengfei
    date: 07/06/2017
    """
    thefile = open('C:/Users/pli006/Documents/Sourcetree/review_cluster/raw_data/' + filename, 'w')
    for sentence in file:
        thefile.write("%s\n" % sentence)
    thefile.close()


if __name__ == '__main__':

    corpus = read_Surveycsv('C:/Users/pli006/Documents/Sourcetree/review_cluster/raw_data/survey_data.csv')

    fileWriter("q1.txt", corpus[1][0])
    fileWriter("q2.txt", corpus[2][0])
    fileWriter("q3.txt", corpus[3][0])
    fileWriter("q4.txt", corpus[4][0])
    fileWriter("q5.txt", corpus[5][0])
    fileWriter("q6.txt", corpus[6][0])
    fileWriter("q7.txt", corpus[7][0])
    fileWriter("q8.txt", corpus[8][0])
    fileWriter("q9.txt", corpus[9][0])
    fileWriter("q10.txt", corpus[10][0])
