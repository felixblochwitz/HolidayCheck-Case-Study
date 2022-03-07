import requests as req
import pandas as pd
import json

from datetime import datetime
from datetime import timedelta
from datetime import date

import warnings
warnings.filterwarnings("ignore")


def get_articles(query, start_date, api_key):
    """scrapes all articles from guardian api from start_date
       until day before today

       save dataset as csv as "trudeau.csv"

       is used to create initial dataset of articles. for any
       subsequent updates use update_articles function

    Args:
        query (str): query
        start_date (str): start date
        api_key (str): api-key for the guardian api

    Returns:
        pandas.DataFrame: Pandas dataframe containing all articles
                          and meta information
    """
    to_date = date.today() - timedelta(days=1)
    api_str = f'https://content.guardianapis.com/search?q="{query}"&from-date={start_date}&to-date={to_date}&order-by=oldest&api-key={api_key}&type=article&page-size=50&show-fields=body&query-fields=headline'
    response = json.loads(req.get(api_str).content)

    # create dataframe
    cols = ['id', 'type', 'sectionId', 'sectionName',
            'webPublicationDate', 'webTitle', 'webUrl', 'body']
    df = pd.DataFrame(columns=cols)

    # iterate over entries in json response and write to df
    pages = response['response']['pages']
    keys = ['id', 'type', 'sectionId', 'sectionName',
            'webPublicationDate', 'webTitle', 'webUrl']

    for i in range(1, pages + 1):
        response = json.loads(req.get(api_str + f'&page={i}').content)

        for entry in response['response']['results']:
            write_entry = {k: entry[k] for k in keys}
            write_entry['body'] = entry['fields']['body']
            df = df.append(write_entry, ignore_index=True)

    # convert webPublicationDate column to datetime objects
    df['webPublicationDate'] = pd.to_datetime(df['webPublicationDate'])
    # create column with local time
    df['dateTimeLocal'] = df['webPublicationDate'].dt.tz_convert(
        tz='Europe/Berlin')
    # strip article bodies from html tags
    df['body'] = df['body'].str.replace(r'<.*?>', '', regex=True)
    # write dataframe to csv
    df.to_csv('trudeau.csv', index=False)

    return df


def group_days(df=None, csv_path=None):
    """groups samples by day and counts the number of articles
       published per day
       give either csv path or pandas dataframe as argument

       save dataset as csv as "trudeau_grouped.csv"

    Args:
        df (pandas.DataFrame, optional): dataframe. Defaults to None.
        csv_path (_type_, optional): dataset as csv. Defaults to None.

    Returns:
        Pandas.Dataframe: a dataframe grouped by day and counts of
                          articles per day
    """
    if not csv_path == None:
        df = pd.read_csv(csv_path)

    df = df.set_index('webPublicationDate')
    df_grouped = df.groupby(pd.to_datetime((df.index.date))).size(
    ).reset_index(name='numberOfArticles')
    df_grouped.set_index('index', inplace=True)

    date_range = pd.date_range(
        datetime(2018, 1, 1), datetime.today() - timedelta(days=1))
    df_grouped = df_grouped.reindex(index=date_range, fill_value=0)
    df_grouped = df_grouped.reset_index().rename(columns={'index': 'date'})
    df_grouped['date'] = df_grouped.date.dt.tz_localize('UTC')

    df_grouped.to_csv('trudeau_grouped.csv', index=False)

    return df_grouped


def update_articles(df, query, api_key):
    """updates articles datafram with newly released articles 
       the day before today

       save dataset as csv as "trudeau.csv"

    Args:
        df (Pandas.DataFrame): dataframe
        query (str): query
        api_key (str): api-key for guardian api

    Returns:
        Pandas.DataFrame: updated dataframe of articles
    """
    query_date = date.today() - timedelta(days=2)

    api_str = f'https://content.guardianapis.com/search?q="{query}"&from-date={query_date}&to-date={query_date}&order-by=oldest&api-key={api_key}&type=article&page-size=50&show-fields=body&query-fields=headline'
    response = json.loads(req.get(api_str).content)

    pages = response['response']['pages']
    keys = ['id', 'type', 'sectionId', 'sectionName',
            'webPublicationDate', 'webTitle', 'webUrl']

    for i in range(1, pages + 1):
        response = json.loads(req.get(api_str + f'&page={i}').content)

        for entry in response['response']['results']:
            write_entry = {k: entry[k] for k in keys}
            write_entry['body'] = entry['fields']['body']
            df = df.append(write_entry, ignore_index=True)

    # convert webPublicationDate column to datetime objects
    df['webPublicationDate'] = pd.to_datetime(df['webPublicationDate'])
    # create column with local time
    df['dateTimeLocal'] = df['webPublicationDate'].dt.tz_convert(
        tz='Europe/Berlin')
    # strip article bodies from html tags
    df['body'] = df['body'].str.replace(r'<.*?>', '', regex=True)
    # write dataframe to csv
    df.to_csv('trudeau.csv', index=False)

    return df
