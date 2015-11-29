__author__ = 'alanseciwa'
# Reference: Raj Kesavan @ http://www.rajk.me

import datetime
import json
import sys
import pandas as pd
import tweepy
from textblob import TextBlob

from candidate_list import clist
from private_keys import consumer_key, consumer_secret, access_token, access_token_secret
from spam_detection import SpamBotDetection

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# wait_on_rate_limit is set to true so that I could avoid hitting the rate limit
api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

# anonymous function called term
# Returns tweets that match a specified query. rpp is the # of tweets to return per page
cursor = lambda term: tweepy.Cursor(api.search, q = term, rpp = 100)

def tweet_to_dict_spam(tweet, candidate):

    # Check for Twitter-SpamBot
    bot = SpamBotDetection()

    dict = {
        'candidate': candidate,
        'id': tweet.id,
        'coordinates': tweet.coordinates,
        'favorite_count': tweet.favorite_count,
        'created_at': tweet.created_at,
        'geo': tweet.geo,
        'lang': tweet.lang,
        'place': tweet.place,
        'retweet_count': tweet.retweet_count,
        'text': tweet.text,
        'user_created_at': tweet.user.created_at,
        'user_statuses_count': tweet.user.statuses_count,
        'user_location': tweet.user.location,
        'user_name': tweet.user.name,
        'user_screen_name': tweet.user.screen_name,
        'user_time_zone': tweet.user.time_zone,
        'user_followers_count': tweet.user.followers_count,
        'user_follower_ratio': float(tweet.user.followers_count) / float(tweet.user.friends_count),
        'user_description': tweet.user.description
    }

    # assign tweet values to variables
    u_c_a = tweet.user.created_at
    u_s_c = tweet.user.statuses_count
    u_r = float(tweet.user.followers_count) / float(tweet.user.friends_count)
    u_d = tweet.user.description

    # check if Twitter user is a spambot
    if(bot.check_user_date(u_c_a) is False or bot.check_status_count(u_s_c) is False
       or bot.check_ratio(u_r) is False or bot.check_descript_len(u_d) is False):
        dict['is_user_spam'] = 'False'
        return dict
    else:
        dict['is_user_spam'] = 'True'
        return dict


# following functions order and arrange tweets as they come in

def tweets_json(tweets):
    return [tweet._json for tweet in tweets]


def tweets_df(tweets, term, f):
    return pd.DataFrame([f(tweet, term) for tweet in tweets])


def search(cursor, term, number):
    return list(cursor(term).items(number))


if __name__ == '__main__':

    # specify the amount of tweets to collect per candidate
    # e.g. ~$ python retrieve.py 100
    number_per_candidate = 100 #int(sys.argv[1])
    print(number_per_candidate)

    # path to results directory
    path = '/Users/alanseciwa/Desktop/TwitterAPI/tweepy-master/results'

    # dataframes List
    dfs = []

    # dictionary for JSON's key:value pairs
    jsons = {}

    # search for specified candidates in tweets
    for candidate in clist:
        print('Searching for ' + candidate)
        tweets = search(cursor, candidate, number_per_candidate)
        dfs.append(tweets_df(tweets, candidate, tweet_to_dict_spam))
        jsons[candidate] = tweets_json(tweets)

    # assign tweets to pandas dataframes
    df = pd.concat(dfs)
    postfix = str(datetime.datetime.now())

    # output results to specified location/directory
    df.to_csv(path+'/results-{}.csv'.format(postfix))
    with open(path+'/results-{}.json'.format(postfix), 'w') as json_file:
        json_file.write(json.dumps(jsons))
