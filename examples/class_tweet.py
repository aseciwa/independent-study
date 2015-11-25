from datetime import datetime, timedelta

class SpamBotDetection():
    ''' Detected if tweeter is a spam bot
    '''

    date = None

    '''
    def check_date(self, date_str):
        one_day_ago = datetime.now() - timedelta(days=1)

        if date_str < one_day_ago:
            return True
        else:
            return False
    '''