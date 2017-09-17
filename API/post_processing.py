from collections import Counter

def df_count(corpus):
    text = []
    for comment in corpus:
        text = text + comment[0]
    df = Counter(text)
    return df
