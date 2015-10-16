__author__ = 'alanseciwa'
import sys, os
import json
import csv

def parse_json_data(data):

    csv_file = open('/Users/alanseciwa/Desktop/clean_data-TWEETONLY-2.csv', 'w')
    writer = csv.writer(csv_file, quoting=csv.QUOTE_NONE)

    # Open json file while reserving a buffer size of 1028
    with open(data, 'r', buffering=1028) as read_json:
        for tweet in read_json:

            # Load json and store key-value pair for text in tweet
            jd = json.loads(tweet)

            try:

                #created_at = jd['created_at']
                tweets = jd['text']
                screen_name = jd['user']['screen_name']
                #followers_count = jd['user']['followers_count']
                #lang = jd['user']['lang']
                #geo = jd['geo']
                #coordinates = jd['coordinates']
                #places = jd['place']


                writer.writerow([tweets])
                #writer.writerow((screen_name, tweet, followers_count, geo, coordinates, places))
                #print(screen_name)
                print(tweets)
            except:
                #print('Error')
                pass

    csv_file.close()


def main():

    tweet_data = '/Users/alanseciwa/Desktop/Independent_Study/Raw_dataR/gop-debate-sep16-2.json'

    parse_json_data(tweet_data)

if __name__ == '__main__':
    main()
    sys.exit()