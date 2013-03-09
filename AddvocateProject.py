import twitterop,kloutop,dbop

#Get twitter users from hardcoded list and gather 80 tweets for each
#TODO: allow config values for list and how many tweets per user
twitterop.getTweets()

#query sql db for users and update all user objects with klout score
kloutop.updateScores()

#close the db when we're done
dbop.close()