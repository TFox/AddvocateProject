import MySQLdb
import keys

# SQL db config
host = keys.getSetting('SQL','host')
user = keys.getSetting('SQL','user')
passwd = keys.getSetting('SQL','passwd')
dbid = keys.getSetting('SQL','dbid')

# Open the db connection, open a new cursor object. Commits must be made manually
# by calling commit() below.
db = MySQLdb.connect(host=host,user=user,passwd=passwd,db=dbid)
cursor = db.cursor()

# Adds a twitter user to the sql db. Requires id and screen_name attributes
def addUser(user):
    sql = "INSERT IGNORE INTO users (id,screen_name) VALUES (%s,%s)"
    cursor.execute(sql,(user.id,user.screen_name))

# Get all id and screen_names from the database. Used for updating klout score
def getUsers():
    cursor.execute("SELECT id,screen_name FROM users")
    return cursor.fetchall()

# Add tweet content to the db. Since tweepy gives us back the creator's info, we
# can add the user.id to this table without requiring a user object. Also included are
# Tweet id, tweet text, and retweet_count from the tweepy object.
def addTweet(content):
    sql = "INSERT IGNORE INTO tweets (id,user_id,text,retweets) VALUES (%s,%s,%s,%s)"
    cursor.execute(sql,(content.id,content.user.id,content.text.encode('ascii', 'ignore'),content.retweet_count))

# Apdate the sql db with current klout score. The users are pulled from the db originally,
# so we shouldn't have to check if they exist.
def updateKloutScore(userid,score):
    sql = "UPDATE users SET klout_score = %s WHERE id = %s"
    cursor.execute(sql,(score,userid))

# Commit changes made by the cursor above.
def commit():
    db.commit()

# Close the db when we're done.
def close():
    db.close()

# On creation of the class, make sure the tables we need are ready to go.
# This bit can be removed in frequent-use scenarios
cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                        id BIGINT NOT NULL PRIMARY KEY,
                        screen_name VARCHAR(50),
                        klout_score INT,
                        klout_reliability INT)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS tweets (
                        id BIGINT NOT NULL PRIMARY KEY,
                        user_id BIGINT NOT NULL,
                        text VARCHAR(255),
                        retweets INT)""")
commit()