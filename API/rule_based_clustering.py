def clustering(corpus, question):
    clustered_index = []
    # rule list order: high priority to low priority
    if question == 3:
        cluster_rule_list = ['detail', 'updat', 'advis', 'commit', 'behavior', 'knowledg', 'train', 'guid', 'question', \
                             'information', 'inform', 'respond']
    elif question == 6:
        cluster_rule_list = ['bu', 'shop', 'food', 'board', 'transport']

    for word in cluster_rule_list:
        idx_set = []
        for idx, doc in enumerate(corpus):
            if word in doc[0] and idx not in clustered_index:
                idx_set.append(idx)
                corpus[idx] = corpus[idx] + (word,)
        clustered_index = clustered_index + idx_set
    clustered_index = set(clustered_index)
    unclustered_index = list(set(range(len(corpus))) - clustered_index)
    print "No. of clustered sentences by rules:", len(clustered_index)
    print "No. of unclustered sentences:", len(unclustered_index)

    return unclustered_index, corpus


