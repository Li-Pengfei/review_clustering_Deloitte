import survey_reader
import pre_processing

def process_question(ques_num, csv_path):
    content = survey_reader.read_Surveycsv(csv_path)[ques_num]
    print 'Length of content', len(content)

    switcher = {
        1: "q1", 2: "q2", 3: "q3", 4: "q4", 5: "q5", 6: "q6",
        7: "q7", 8: "q8", 9: "q9", 10: "q10"
    }
    # Get the function from switcher dictionary to process corresponding question
    func = switcher.get(ques_num, lambda: "Question number must between 1-10 (inclusive)!")
    # Execute the function
    return func(content, csv_path)

def q1(content, csv_path):
    print 'q2'
    return

def q3(content, csv_path):
    pos_tags = ['NN', 'NNS', 'JJ', 'JJR', 'JJS']
    doc_noimprove, doc_extracted, doc_other = pre_processing.process_corpus(content, pos_tags, question='3')






