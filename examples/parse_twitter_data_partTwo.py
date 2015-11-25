__author__ = 'alanseciwa'
import sys
import json
import csv
from datetime import datetime, timedelta
from textblob import TextBlob
from elasticsearch import Elasticsearch


es = Elasticsearch()

class SpamBodDetection():
    """Check if twitter user is a spambot.
       Check user date creation, check the total number of tweets, Check the friends to followers ratio,
       and check the user description if its more than a few words
    """

    def check_user_date(self, date_str):
        one_day_ago = datetime.now() - timedelta(days=1)

        if date_str < one_day_ago:
            return True
        else:
            return False

    def check_status_count(self, status):

        if int(status) < 50:
            return True
        else:
            return False

    def check_ratio(self, ratio):
        if ratio < 0.01:
            return True
        else:
            return False

    def check_descript_len(self, description):
        if len(description) < 20:
            return True
        else:
            return False


def check_obj(c):
    if not c:
        c = ''
    else:
        c = c

    return c


def parse_json_data(data):

    csv_file = open('/Users/alanseciwa/Desktop/clean_data-TWEETONLY-2.csv', 'w')
    writer = csv.writer(csv_file, quoting=csv.QUOTE_NONE)

    bot = SpamBodDetection()

    # Open json file while reserving a buffer size of 1024
    with open(data, 'r', buffering=1024) as read_json:
        for tweet in read_json:

            # Load json and store key-value pair for text in tweet
            jd = json.loads(tweet)

            try:

                #tweets = TextBlob(jd['text'])
                tweets = jd['text']

                #tweet_date = jd['created_at']
                screen_name = jd['user']['screen_name']
                #lang = jd['user']['lang']
                #geo = jd['geo']

                # User information
                user_created_at = datetime.strptime(jd['user']['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
                user_statuses_count = jd['user']['statuses_count']
                user_ratio = float(jd['user']['followers_count']) / float(jd['user']['friends_count'])
                user_description = jd['user']['description']

                # Location and Lang.
                #coordinates = jd['coordinates']
                #places = jd['place']
                #geo = jd['geo']
                #lang = jd['user']['lang']


                #check_if_spambot()

                # Output sentiment polarity
                #print(tweets.sentiment.polarity)

                # Determine if sentiment is positive, negative, or neutral
                '''
                if tweets.sentiment.polarity < 0:
                    sentiment = 'negative'
                elif tweets.sentiment.polarity == 0:
                    sentiment = 'neutral'
                else:
                    sentiment = 'positive'

                # Print output
                print(sentiment)

                # add text and sentiment info to elasticsearch
                es.index(index="sentiment",
                         doc_type="text-type",
                         body={"message": jd["text"],
                               "polarity": tweets.sentiment.polarity,
                               "subjectivity": tweets.sentiment.subjectivity,
                               "sentiment": sentiment})
                return True
                '''
                #writer.writerow([tweets_encode])
                #writer.writerow((screen_name, tweet, followers_count, geo, coordinates, places))
                #print(screen_name)
                #print(tweets_encode)
            except:
                #print('Error')
                pass

    csv_file.close()


def main():

    #tweet_data = '/Users/alanseciwa/Desktop/Independent_Study/Raw_data/gop-debate-sep16-2.json'
    #tweet_data = '/Users/alanseciwa/Desktop/Independent_Study/Raw_data/gop-debate-sep16-2.json'
    tweet_data = '/Users/alanseciwa/Desktop/sample.json'

    parse_json_data(tweet_data)

if __name__ == '__main__':
    main()
    sys.exit()