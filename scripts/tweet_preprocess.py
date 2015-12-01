__author__ = 'alanseciwa'

import re
import numpy as np
import pandas as pd
from textblob import TextBlob
from candidate_list import clist

def clean(df):
    # go through candidate name list
    df = df[df.candidate.isin(clist)]
    del df['Unnamed: 0']

    return df


def datetimeify(df):
    # get created time of tweet
    df['created_at'] = pd.DatetimeIndex(df.created_at)

    return df


def sentiment(df):
    ''' This function assigns sentiment values. It check if the tweet (text) is
        is negative, neutral, or positive. In addition, it check either if the tweet
        is subjective.
        TextBlob is the does the heavy lifting.
    '''
    tweet = df.dropna(subset=['text']).text
    sentiment = tweet.apply(lambda tweet: TextBlob(tweet).sentiment)
    df['polarity'] = sentiment.apply(lambda sentiment: sentiment.polarity)
    df['subjectivity'] = sentiment.apply(lambda sentiment: sentiment.subjectivity)
    return df


def influence(df):
    # get influence score for the amount of followers a user and the amount
    # of retweets a user has.
    friends = np.sqrt(df.user_followers_count.apply(lambda x: x + 1))
    retweets = np.sqrt(df.retweet_count.apply(lambda x: x + 1))

    df['influence'] = friends * retweets

    return df


def influenced_polarity(df):
    # get influenced polarity score by multiplying polarity score
    # with influence score

    df['influenced_polarity'] = df.polarity * df['influence']
    return df


def georeference(df):
    # Get geo coordinates from each tweet
    def place_to_coordinate(pl_str, kind):

        if(pd.isnull(pl_str)):
            return float('nan')

        # use regex to find coordinate number
        num_matcher = r'(-?\d+\.\d+)[,\]]'
        coordinates = re.findall(num_matcher, pl_str)
        coordinate = tuple(float(n) for n in coordinates[:2])

        if(kind == 'longitude'):
            return coordinate[0]
        elif(kind == 'latitude'):
            return coordinate[1]

    df['latitude'] = df.place.apply(place_to_coordinate, kind='latitude')
    df['longitude'] = df.place.apply(place_to_coordinate, kind='longitude')

    return df


def preprocess(df):
    # return processes
    return (df.pipe(datetimeify)
              .pipe(sentiment)
              .pipe(influence)
              .pipe(influenced_polarity)
              .pipe(georeference))


def preprocess_df(df):
    # clean data
    cleaned = df.pipe(clean)
    copy = cleaned.copy()

    return preprocess(copy)


def load_df(input_filename):

    raw_df = pd.read_csv(input_filename, engine='python')
    return preprocess_df(raw_df)
