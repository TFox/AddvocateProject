import keys
from klout import *
import dbop

# Set the Klout auth key
klout = Klout(keys.getSetting('Klout', 'key'),secure=True)

# Grab scores for each klout user currently in the sql db. Sets -1 for
# scores that are unavailable
def updateScores():
    users = dbop.getUsers()
    for user in users:
        try:
            id = klout.identity.klout(screenName=user[1]).get('id')
            score = klout.user.score(kloutId=id).get('score')
            dbop.updateKloutScore(user[0], score)
            print user[1]
        # TODO: expand the error handling a bit to register a difference between
        # unavailable klout score and other problems such as auth failure or
        # service interruption
        except:
            dbop.updateKloutScore(user[0], -1)