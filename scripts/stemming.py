from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize,
import sys

def remove_stopwords(tweets):

    stemmer = PorterStemmer()

     with open(tweets, 'r', buffering=1028) as read_tweet:
        for tweet in read_tweet:

            #Use stop word method
            stop_words = set(stopwords.words('english'))
            word_tokens = word_tokenize(tweet)

            filtered_tweet = []

            for word in word_tokens:
                if word not in stop_words:
                    # Capture only words not listed in stop_word txt
                    filtered_tweet.append(word)

            print(filtered_tweet)


def main():

    tweets = "/Users/alanseciwa/Desktop/Independent_Study/Sep16-GOP-TweetsONLY/clean_data-TWEETONLY.csv"

    remove_stopwords(tweets)

if __name__ == '__main__':
    main()
    sys.exit()