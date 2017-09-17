import string
import numpy as np
import pandas as pd
import nltk
import cPickle
import data_helper
# from keras.preprocessing import sequence
from sklearn import preprocessing


def read_Surveycsv(filepath):
    """
        author: Pengfei
        date: 07/06/2017
    """
    df = pd.read_csv(filepath, usecols=['Q3_1', 'Q3_2', 'Q3_3', 'Q3_4', 'Q3_5', 'Q3_6', 'Q3_7', 'Q3_8', 'Q3_9', 'Q3_10',
                                        'Q4', 'Q5'])
    print(df.describe())

    q4 = df['Q4'].astype('category')
    print("\nCount summary for each question:")
    print(q4.value_counts())

    q5 = df['Q5']

    idx_bool_Noimprovement = q4 == "No improvement require"
    idx_Noimprovement = [i for i, bool in enumerate(idx_bool_Noimprovement) if bool]
    q5_Noimprovement = q5[q4 == "No improvement require"].tolist()
    corpus_Noimprovement = [data_helper.clean_str(sent) for sent in q5_Noimprovement]

    idx_bool_Charges = q4 == "The charges you paid for the last service"
    idx_Charges = [i for i, bool in enumerate(idx_bool_Charges) if bool]
    q5_Charges = q5[q4 == "The charges you paid for the last service"].tolist()
    corpus_Charges = [data_helper.clean_str(sent) for sent in q5_Charges]

    idx_bool_Location = q4 == "The dealership location"
    idx_Location = [i for i, bool in enumerate(idx_bool_Location) if bool]
    q5_Location = q5[q4 == "The dealership location"].tolist()
    corpus_Location = [data_helper.clean_str(sent) for sent in q5_Location]

    idx_bool_VehicleCondition = q4 == "The condition and cleanliness of vehicle when you received your vehicle after servicing"
    idx_VehicleCondition = [i for i, bool in enumerate(idx_bool_VehicleCondition) if bool]
    q5_VehicleCondition = q5[
        q4 == "The condition and cleanliness of vehicle when you received your vehicle after servicing"].tolist()
    corpus_VehicleCondition = [data_helper.clean_str(sent) for sent in q5_VehicleCondition]

    idx_bool_TimeTaken = q4 == "The total time taken to complete the servicing of your vehicle"
    idx_TimeTaken = [i for i, bool in enumerate(idx_bool_TimeTaken) if bool]
    q5_TimeTaken = q5[q4 == "The total time taken to complete the servicing of your vehicle"].tolist()
    corpus_TimeTaken = [data_helper.clean_str(sent) for sent in q5_TimeTaken]

    idx_bool_OpeningTime = q4 == "Dealership opening/closing days and time"
    idx_OpeningTime = [i for i, bool in enumerate(idx_bool_OpeningTime) if bool]
    q5_OpeningTime = q5[q4 == "Dealership opening/closing days and time"].tolist()
    corpus_OpeningTime = [data_helper.clean_str(sent) for sent in q5_OpeningTime]

    idx_bool_WaitingArea = q4 == "The waiting area (e.g., comfort, cleanness, facilities)"
    idx_WaitingArea = [i for i, bool in enumerate(idx_bool_WaitingArea) if bool]
    q5_WaitingArea = q5[q4 == "The waiting area (e.g., comfort, cleanness, facilities)"].tolist()
    corpus_WaitingArea = [data_helper.clean_str(sent) for sent in q5_WaitingArea]

    idx_bool_Quality = q4 == "Quality of the work performed on your vehicle (e.g., fixing of issues during this servicing visit)"
    idx_Quality = [i for i, bool in enumerate(idx_bool_Quality) if bool]
    q5_Quality = q5[
        q4 == "Quality of the work performed on your vehicle (e.g., fixing of issues during this servicing visit)"].tolist()
    corpus_Quality = [data_helper.clean_str(sent) for sent in q5_Quality]

    idx_bool_FollowUp = q4 == "The follow-up calls made by the dealership post servicing of your vehicle to check your service experience and car condition"
    idx_FollowUp = [i for i, bool in enumerate(idx_bool_FollowUp) if bool]
    q5_FollowUp = q5[
        q4 == "The follow-up calls made by the dealership post servicing of your vehicle to check your service experience and car condition"].tolist()
    corpus_FollowUp = [data_helper.clean_str(sent) for sent in q5_FollowUp]

    idx_bool_Explanations = q4 == "The explanations given by dealership staff during your service visit (e.g., helpful/detailed)"
    idx_Explanations = [i for i, bool in enumerate(idx_bool_Explanations) if bool]
    q5_Explanations = q5[
        q4 == "The explanations given by dealership staff during your service visit (e.g., helpful/detailed)"].tolist()
    corpus_Explanations = [data_helper.clean_str(sent) for sent in q5_Explanations]

    idx_bool_Appointment = q4 == "Arranging service appointment/visits to the dealership"
    idx_Appointment = [i for i, bool in enumerate(idx_bool_Appointment) if bool]
    q5_Appointment = q5[q4 == "Arranging service appointment/visits to the dealership"].tolist()
    corpus_Appointment = [data_helper.clean_str(sent) for sent in q5_Appointment]

    return [[corpus_Noimprovement, idx_Noimprovement], [corpus_Appointment, idx_Appointment], [corpus_OpeningTime, idx_OpeningTime],
            [corpus_Explanations,idx_Explanations], [corpus_VehicleCondition, idx_VehicleCondition],
            [corpus_Quality, idx_Quality], [corpus_Location, idx_Location], [corpus_WaitingArea, idx_WaitingArea],
            [corpus_TimeTaken, idx_TimeTaken], [corpus_Charges, idx_Charges], [corpus_FollowUp, idx_FollowUp]]


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
