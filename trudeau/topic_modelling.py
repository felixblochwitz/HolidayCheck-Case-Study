def lda(dfs):
    """topic modelling for dataset article bodies.
       intended to work on multiple datasets, single dataset
       has to be given as list of len=1

    Args:
        dfs (list): list of Pandas.DataFrames

    Returns:
        list: deteced topics and the most descriptive words
    """
    from gensim.models import Phrases
    from gensim import corpora
    from gensim import models

    topic_list = []

    for df in dfs:
        tokens = df.lemmas.tolist()
        bigram_model = Phrases(tokens)
        tokens = [bigram_model[text] for text in tokens]

        LDA_dict = corpora.Dictionary(tokens)
        # LDA_dict.filter_extremes(no_below=3)
        corpus = [LDA_dict.doc2bow(t) for t in tokens]

        num_topics = 1
        lda_model = models.LdaModel(corpus, num_topics=num_topics, \
                                        id2word=LDA_dict, \
                                        passes=4, alpha=[0.01]*num_topics, \
                                        eta=[0.01]*len(LDA_dict.keys()))
        topic_list.append(lda_model.show_topics(num_words=10))

    return topic_list