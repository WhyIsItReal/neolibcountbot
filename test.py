import praw
import time
import os
import requests

reddit = praw.Reddit(client_id=os.environ['H_CLIENT_ID'],
                     client_secret=os.environ['H_CLIENT_SECRET'],
                     user_agent=os.environ['H_USER_AGENT'],
                     password=os.environ['REDDIT_PASSWORD'],
                     username='neolibcountbot')


def main():
    print(reddit.read_only, reddit.user.me())

    getInbox()


def getInbox():
    for message in reddit.inbox.unread(limit=None):
        message.mark_read()
        count = 0
        body = str(message.body).lower()
        if body.startswith("/u/neolibcountbot"):
            name = ""
            print("contains my name!")
            rest = body[17:]
            if rest.startswith(" /u/neolibcountbot"):
                print("show stats")
                if totalUsers != 0:
                    print("So far, " + str(totalUsers) + " have been queried, and have collectively said the n-word " + str(
                        totalCount) + " times, for an average of " + str(float(totalCount/totalUsers)) + " times per user.")
            elif rest.startswith(" /u/"):
                name = rest[4:]
                redditor1 = reddit.redditor(name)
                try:
                    for comment in redditor1.comments.new(limit=None):
                        testing = str(comment.body).lower()
                        if testing.__contains__("neolib"):
                            print(testing)
                            lCount = testing.count("neolib")
                            count += lCount
                    totalCount += count
                    totalUsers += 1
                except:
                    print("failed, continue anyway")

                print(str(message.body)
                      [18:] + " has said n\\*\\*l\\*b\\*r\\*l " + str(count) + " times.")
                message.reply(str(message.body)
                              [18:] + " has said n\\*\\*l\\*b\\*r\\*l " + str(count) + " times.")

            elif rest == "":
                print("show stats!")
            else:
                print("invalid command")

        else:
            print("invalid command")


main()
