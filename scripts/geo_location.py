__author__ = 'alanseciwa'
import sys, os
import nltk
import json
import pandas as pd

def parse_json_data(data):


    with open(data, 'r') as read_json:
        for i in read_json:

            # Load json and store key value pair for text in tweet
            jd = json.loads(i)

            created_at = jd['created_at']
            tweet = jd['text']
            screen_name = jd['user']['screen_name']
            followers_count = jd['user']['followers_count']
            lang = jd['user']['lang']
            geo = jd['geo']
            coordinates = jd['coordinates']
            places = jd['place']

            #data = [created_at, tweet, screen_name, followers_count, lang, geo, coordinates, places]
            #df = pd.DataFrame(data, columns=['created_at', 'tweet', 'screen_name', 'f_count', 'lang', 'geo', 'coordinates', 'place'])
            #df = pd.to_csv('/Users/alanseciwa/Desktop/sample.csv', sep=',')

            print(coordinates, places)

            # Tokenize tweet (split every word).
            #tokenized = nltk.word_tokenize(tweet)
            #tagged = nltk.pos_tag(tokenized)    # parts of speech tags

            #print(tagged)


def main():
    if os.path.isfile('/Users/alanseciwa/Desktop/gop-debate-bottom4-sep16.json'):
        load_data = '/Users/alanseciwa/Desktop/gop-debate-bottom4-sep16.json'
        parse_json_data(load_data)

    else: print('No')

if __name__ == '__main__':
    main()
    sys.exit()
