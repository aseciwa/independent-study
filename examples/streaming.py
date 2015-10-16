#!/user/bin/python

from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import time

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key="9Bix7oCZz8TyC7hsjnRSiBmfr"
consumer_secret="RCdJg1UNkDFFAns9j9hYKQe0agO97asBBP4VVVeciICZANmzQW"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="180419137-qeoBTFNlpPj1PCZZuW01Q4Ckl8oTI2aXK7eBkxAF"
access_token_secret="LhqHARMJQgX1HXnMQuSj2BizgxPZgKrBdyAJtTVVJv0X7"

class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    def on_data(self, data):

        try:
            # Append json data to specified output file
            with open('/Users/alanseciwa/Desktop/gop-debate-sep16-2.json', 'a') as out_append:
                out_append.write(data)

            print(data)
            return True
        
        except BaseException as e:
            print('Failed on data: %s' % str(e))
            time.sleep(11)


    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=['GOP', 'GOP Debate', '#GOPDebate'])
