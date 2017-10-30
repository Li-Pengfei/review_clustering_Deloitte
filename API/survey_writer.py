import string
import numpy as np
import pandas as pd
import nltk
import cPickle
import data_helper
# from keras.preprocessing import sequence
from sklearn import preprocessing
import csv
import os.path

def rule_all(tt_list):
    tt_list = ['others' if x == (None, None) else x for x in tt_list]
    tt_list = list(set(tt_list))
    if len(tt_list)>1 and 'others' in tt_list:
        tt_list.remove('others')
    return tt_list


def write_Label(content, listuple, csv_path, index):
    ##creating pandas
    idx_comment = range(len(content))
    df_comment = pd.DataFrame({'id': idx_comment, 'comment': content})
    df_survey = pd.DataFrame(listuple, columns=['sentence', 'id', 'label'])
    df_all = pd.merge(df_comment, df_survey, on='id', how='inner')
    df_final = df_all.groupby(['id', 'comment'])['label'].apply(list).to_frame()

    df_final['label'] = df_final['label'].apply(lambda x: rule_all(x))
    # df_final.to_csv(csv_path)

    ### Write label to original CSV file
    with open(csv_path, 'r') as csvinput:
        reader = csv.reader(csvinput)
        all = []
        row = next(reader)
        if len(row) == 36:
            row.append('Class_Label')
        all.append(row)

        count = 0
        for i, row in enumerate(reader):
            if i in index and len(row) == 36:
                row.append(df_final['label'].values[count])
                count += 1
            all.append(row)
    with open(csv_path, 'w') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        writer.writerows(all)

def write_Cluster_Info(cluster_info_all, cluster_info_path):
    df_cluster_info = pd.DataFrame(cluster_info_all, columns=['question', 'cluster_label', 'frequency', 'sentence_exemplar'])
    question = df_cluster_info['question'].values[0]

    if os.path.exists(cluster_info_path):
        with open(cluster_info_path, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            questions = set([int(row[0]) for row in reader])
            if question in questions:
                return
            else:
                with open(cluster_info_path, 'a') as f:
                    df_cluster_info.to_csv(f, header=False, index=False)

    else:
        df_cluster_info.to_csv(cluster_info_path, index=False)



# if __name__ == '__main__':
