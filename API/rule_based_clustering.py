def clustering(corpus, question):
    clustered_index = []
    label = {}
    # rule list order: high priority to low priority
    if question == 3:
        cluster_rule_list = ['detail', 'updat', 'advis', 'commit', 'behavior', 'knowledg', 'train', 'guid', 'question', \
                             'information', 'inform', 'respond']

    for word in cluster_rule_list:
        idx_set = []
        for idx, doc in enumerate(corpus):
            if word in doc and idx not in clustered_index:
                idx_set.append(idx)
                label[idx] += word
            name_list[word] = idx_set
            clustered_index = clustered_index + idx_set

    clustered_index = set(clustered_index)
    unclustered_index = list(set(range(len(nn_extracted))) - clustered_index)
    print "No. of clustered sentences:", len(clustered_index)
    print "No. of unclustered sentences:", len(unclustered_index)


