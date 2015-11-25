__author__ = 'alanseciwa'

import re
import csv
import os
import sys

def match_values(u_list, v_list, t_list):

    re_pattern = re.compile(u'['
                            u'\U0001F300-\U0001F5FF'
                            u'\U0001F600-\U0001F64F'
                            u'\U0001F680-\U0001F6FF'
                            u'\u2600-\u26FF\u2700-\u27BF]+',
                            re.UNICODE)

    for i in t_list:

        if re_pattern.sub('', i):

            print(i)
        else:
            print("no")



def hex_to_values(tweet, hex_values):

    # Put hex values and name into list variables
    utf_list = []
    val_list = []

    with open(hex_values, 'r') as h_values:

        csv_reader = csv.reader(h_values)

        for values in csv_reader:
            utf_list.append(values[0])
            val_list.append(values[2])


    tweet_list = []

    with open(tweet, buffering=1024) as string_tweets:
        for t in string_tweets:
            tweet_list.append(t)


    # Send lists to match_values
    match_values(utf_list, val_list, tweet_list)


def main():

    # Tweet location
    tweets = "/Users/alanseciwa/Desktop/cleaned.csv"
    hex_values = "/Users/alanseciwa/Desktop/hex_emoji_values.csv"

    hex_to_values(tweets, hex_values)


if __name__ == '__main__':
    main()
    sys.exit()