import string
import numpy as np
import pandas as pd
import nltk
import cPickle
import data_helper
from keras.preprocessing import sequence
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

    q5_Noimprovement = q5[q4 == "No improvement require"].tolist()
    corpus_Noimprovement = [data_helper.clean_str(sent) for sent in q5_Noimprovement]

    q5_Charges = q5[q4 == "The charges you paid for the last service"].tolist()
    corpus_Charges = [data_helper.clean_str(sent) for sent in q5_Charges]

    q5_Location = q5[q4 == "The dealership location"].tolist()
    corpus_Location = [data_helper.clean_str(sent) for sent in q5_Location]

    q5_VehicleCondition = q5[
        q4 == "The condition and cleanliness of vehicle when you received your vehicle after servicing"].tolist()
    corpus_VehicleCondition = [data_helper.clean_str(sent) for sent in q5_VehicleCondition]

    q5_TimeTaken = q5[q4 == "The total time taken to complete the servicing of your vehicle"].tolist()
    corpus_TimeTaken = [data_helper.clean_str(sent) for sent in q5_TimeTaken]

    q5_OpeningTime = q5[q4 == "Dealership opening/closing days and time"].tolist()
    corpus_OpeningTime = [data_helper.clean_str(sent) for sent in q5_OpeningTime]

    q5_WaitingArea = q5[q4 == "The waiting area (e.g., comfort, cleanness, facilities)"].tolist()
    corpus_WaitingArea = [data_helper.clean_str(sent) for sent in q5_WaitingArea]

    q5_Quality = q5[
        q4 == "Quality of the work performed on your vehicle (e.g., fixing of issues during this servicing visit)"].tolist()
    corpus_Quality = [data_helper.clean_str(sent) for sent in q5_Quality]

    q5_FollowUp = q5[
        q4 == "The follow-up calls made by the dealership post servicing of your vehicle to check your service experience and car condition"].tolist()
    corpus_FollowUp = [data_helper.clean_str(sent) for sent in q5_FollowUp]

    q5_Explanations = q5[
        q4 == "The explanations given by dealership staff during your service visit (e.g., helpful/detailed)"].tolist()
    corpus_Explanations = [data_helper.clean_str(sent) for sent in q5_Explanations]

    q5_Appointment = q5[q4 == "Arranging service appointment/visits to the dealership"].tolist()
    corpus_Appointment = [data_helper.clean_str(sent) for sent in q5_Appointment]

    return [corpus_Noimprovement, corpus_Appointment, corpus_OpeningTime, corpus_Explanations, corpus_VehicleCondition,
            corpus_Quality, corpus_Location, corpus_WaitingArea, corpus_TimeTaken, corpus_Charges, corpus_FollowUp]


def fileWriter(filename, file):
    """
    author: Pengfei
    date: 07/06/2017
    """
    thefile = open('/data2/Toy_project/survey_content/' + filename, 'w')
    for sentence in file:
        thefile.write("%s\n" % sentence)
    thefile.close()


if __name__ == '__main__':

    corpus = read_Surveycsv('/data2/Toy_project/survey_data.csv')

    fileWriter("q1.txt", corpus[1])
    fileWriter("q2.txt", corpus[2])
    fileWriter("q3.txt", corpus[3])
    fileWriter("q4.txt", corpus[4])
    fileWriter("q5.txt", corpus[5])
    fileWriter("q6.txt", corpus[6])
    fileWriter("q7.txt", corpus[7])
    fileWriter("q8.txt", corpus[8])
    fileWriter("q9.txt", corpus[9])
    fileWriter("q10.txt", corpus[10])
