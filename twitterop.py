import dbop
import keys
import tweepy
import datetime
import time

# Set authentication info for twitter OAuth
auth = tweepy.OAuthHandler(keys.getSetting('Twitter','consumer_key'), keys.getSetting('Twitter','consumer_secret'))
auth.set_access_token(keys.getSetting('Twitter','access_key'), keys.getSetting('Twitter','access_secret'))

# Grab all members from the twitter team list, and the last 90 tweets from each.
# Add the users and tweets to the db as we get them.
# (80 tweets * 1250 users = 100k tweets. 90 tweets each accounts for users with
# lower usage

# TODO: I'd like this to be a little more flexible, allow external config for the list
# we're accessing, how many tweets we grab from each user and separate user/tweet
# processes, if practical
def getTweets():
    timeout = None
    api = tweepy.API(auth)
    # TODO: query the db for user & tweet max values and make sure we don't
    # query for anything we don't need to.
    cursor = tweepy.Cursor(api.list_members, 'twitter', 'team')
    timeout = datetime.datetime.now() + datetime.timedelta(minutes = 15)
    for page in cursor.pages():
        print cursor.iterator.count
        pageDone = False
        while not pageDone:
            try:
                for item in page:
                    try:
                        print datetime.datetime.now(),item.screen_name,item.id
                        dbop.addUser(item)
                        #timeline = api.user_timeline(count=100, user_id = item.id, trim_user=True, include_rts=True)
                        #for tweet in timeline:
                        #    dbop.addTweet(tweet)
                    # Some twitter profiles are private, skip these
                    except tweepy.error.TweepError, e:
                        if e.reason == "Not authorized":
                            continue
                        else:
                            raise e
                    dbop.commit()
                pageDone = True
            # Twitter has rate limits. Wait them out here.
            except tweepy.error.TweepError, e:
                print e.reason
                while datetime.datetime.now() < timeout:
                    time.sleep(1)