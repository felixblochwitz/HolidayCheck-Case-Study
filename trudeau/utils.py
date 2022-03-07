def df_metrics(df, agg_column):
    avg = df[agg_column].mean()
    std = df[agg_column].std()
    total = df[agg_column].sum()
    return avg, std, total


def get_mainsection(df):
    """gets the most common section articles were published in

    Args:
        df (Pandas.DataFrame): dataframe

    Returns:
        str: name of the section
    """
    main_section = df['sectionName'].value_counts().index.tolist()[0]
    return main_section


def preprocess(dfs):
    """preprocesses article bodies for further nlp

    Args:
        dfs (list): list of Pandas.DataFrames

    Returns:
        list: list of Pandas.DataFrames
    """
    import stanza
    stanza.download('en')
    nlp = stanza.Pipeline(
        lang='en', processors='tokenize,mwt,pos,lemma', verbose=False)
    import warnings
    warnings.filterwarnings("ignore")

    # creating lemmatized representation of text bodies
    for df in dfs:
        df['lemmas'] = df['body'].apply(_lemmatize, nlp=nlp)

        # removing stopwords
        from nltk.corpus import stopwords
        my_stopwords = stopwords.words(
            'English') + ['say', 'trudeau', 'justin', 'prime', 'minister', 'canadian', 'canada']
        df['lemmas'] = df['lemmas'].apply(
            lambda x: [y for y in x if y not in my_stopwords])
    return dfs


def _lemmatize(text, nlp):
    """creates lemmatized representation of article bodies only 
       containing nouns, verbs, adjectives and adverbs

    Args:
        text (str): article body to be lemmatized
        nlp (stanza.Pipeline): pre initiated stanza pipeline

    Returns:
        str: lemmatized representation of article body
    """
    doc = nlp(text)
    lemmatized = []
    for sentence in doc.sentences:
        for word in sentence.words:
            if word.upos in ['NOUN', 'VERB', 'ADJ', 'ADV', 'PROPN']:
                lemmatized.append(word.lemma.lower())
    return lemmatized


def outliers_by_std(df, column, window_size, num_stds):
    """creates dataframes of periods with heightened article volume (moving average)

    Args:
        df (Pandas.DataFrame): dataframe
        column (str): name of aggregated column to be examined for outliers
        window_size (int): length of window for moving average
        num_stds (int): number of standard deviations to detect outliers by

    Returns:
        list: list of dataframes
    """
    import pandas as pd
    df[column] = df[column].rolling(window=window_size).mean()
    avg, std = df_metrics(df, column)[:2]
    spikes_df = df.loc[df[column] > avg + num_stds * std]
    groups = spikes_df['date'].diff().gt(f'{window_size} days').cumsum()
    spike_dfs = [x for _, x in spikes_df.groupby(groups)]

    spike_dfs = [df.loc[(df.date > sdf.iloc[0].date - pd.to_timedelta(f'{window_size} days')) &
                        (df.date <= sdf.iloc[-1].date)] for sdf in spike_dfs]
    return spike_dfs


def save_graphic(filename, df):
    """saves a line plot of all articles released from 01.01.2018

    Args:
        filename (str): filename
        df (Pandas.DataFrame): dataframe
    """
    from matplotlib import pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib.ticker import MaxNLocator

    # create year and month locators and formatters
    years = mdates.YearLocator()
    months = mdates.MonthLocator()
    years_fmt = mdates.DateFormatter('%Y')

    fig, ax = plt.subplots()
    fig.set_size_inches(7, 4)
    ax.plot(df.date, df.numberOfArticles)

    ax.xaxis.set_major_formatter(years_fmt)
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_minor_locator(months)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_xlabel('Datum')
    ax.set_ylabel('Anzahl Artikel')

    plt.savefig(f'{filename}.png')
