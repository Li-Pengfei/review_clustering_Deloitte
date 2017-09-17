from collections import Counter

def df_count(corpus):
    text = []
    for comment in corpus:
        text = text + comment
    df = Counter(text)
    return df
