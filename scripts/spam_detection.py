__author__ = 'alanseciwa'

from datetime import datetime, timedelta

class SpamBotDetection():
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

    def check_retweet(self, tweet):
        filters = list('rt and follow', 'rt & follow')