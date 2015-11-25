__author__ = 'alanseciwa'

'''
 This code removes b' characters from utf-8 formatted tweets. This allows tweets to have hex values
 of emojis used in tweets. After stripping away the unwanted characters, it is outputted to a new
 cvs file.
'''
import sys
import csv

def clean(t):

    # set csv file to variable
    csv_file = open('/Users/alanseciwa/Desktop/cleaned.csv', 'w')
    writer = csv.writer(csv_file, quotechar='', quoting=csv.QUOTE_NONE)

    # Open csv file
    with open(t, 'r') as tweet:
        for i in tweet:

            # Use .replace func to filter out all b' chars
            j = i.replace("b'", "").strip() # need strip() func at end to escape char correctly

            # write j to csv writer
            writer.writerow([j])

            print(j)

    csv_file.close()

def main():

    # Tweet location
    tweets = "/Users/alanseciwa/Desktop/clean_data-TWEETONLY-2.csv"

    clean(tweets)

if __name__ == '__main__':
    main()
    sys.exit()