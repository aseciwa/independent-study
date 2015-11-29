#!/user/bin/python

from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from private.private_keys import consumer_key, consumer_secret, access_token, access_token_secret


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


    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=['GOP', 'GOP Debate', '#GOPDebate'])
