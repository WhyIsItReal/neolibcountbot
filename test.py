import praw
import time
import os
import requests
import pyrebase
import json


reddit = praw.Reddit(client_id=os.environ['H_CLIENT_ID'],
                     client_secret=os.environ['H_CLIENT_SECRET'],
                     user_agent=os.environ['H_USER_AGENT'],
                     password=os.environ['REDDIT_PASSWORD'],
                     username='neolibcountbot')


def main():
    print(reddit.read_only, reddit.user.me())

    getInbox()


def getInbox():
    config = json.loads(os.environ['FIREBASE_CONFIG'])
    firebase = pyrebase.initialize_app(config=config)
    db = firebase.database()
    print(db.child('total_count').get().val())

    for message in reddit.inbox.unread(limit=None):
        message.mark_read()
        body = str(message.body).lower()
        if body.startswith("/u/neolibcountbot"):
            name = ""
            print("contains my name!")
            rest = body[17:]
            totalCount = db.child('total_count').get().val()
            totalUsers = db.child('total_users').get().val()

            if rest.startswith(" /u/neolibcountbot"):
                stats(totalCount, totalUsers, message)
            elif rest.startswith(" /u/"):
                name = rest[4:]
                redditor1 = reddit.redditor(name)
                count = 0

                try:
                    for comment in redditor1.comments.new(limit=None):
                        testing = str(comment.body).lower()
                        if testing.__contains__("neolib"):
                            print(testing)
                            lCount = testing.count("neolib")
                            count += lCount
                except:
                    print("failed, continue anyway")

                userCount = db.child('users').child(
                    name).child('total_count').get().val()

                resp = (str(message.body)[18:] + " has said n\\*\\*l\\*b\\*r\\*l " + str(
                    count) + " times.")

                if (userCount == None):
                    # first time dealing with this user
                    print("first time")
                    totalUsers += 1
                    totalCount += count
                    db.child('total_count').set(totalCount)
                    db.child('total_users').set(totalUsers)
                    db.child('users').child(name).child(
                        'total_count').set(count)
                    userCount = 0
                    resp += " This is the first time they have been queried."
                else:
                    # we've seen them before
                    print("compare to old data")
                    if (count != userCount):
                        print("need to update data, smh bad user")
                        totalCount += count - userCount  # increase by the number of new sayings
                        db.child('users').child(name).child(
                            'total_count').set(count)
                        db.child('total_count').set(totalCount)

                        if (count > userCount):
                            resp += " That's an increase of " + \
                                str(count - userCount) + " since last time."
                        else:
                            resp += " That's a decrease of " + \
                                str(userCount - count) + " since last time."
                    else:
                        print("we're done with db stuff")
                        resp += " That's the same as last time."

                print(resp)
                message.reply(resp)

            elif rest == "":
                stats(totalCount, totalUsers, message)
            else:
                print("invalid command")

        else:
            print("invalid command")


def stats(totalCount, totalUsers, message):
    print("show stats")
    print("new total count + users:", totalCount, totalCount)

    resp = ("So far, " + str(totalUsers) + " users have been queried, and have collectively said n\\*\\*l\\*b\\*r\\*l " +
            str(totalCount) + " times, for an average of " + str(float(totalCount/totalUsers)) + " times per user.")
    print(resp)
    message.reply(resp)


main()
