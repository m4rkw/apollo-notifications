#!/usr/bin/env python3

import praw
import pyotp
import json
import os
import pwd
import prawcore.exceptions
import time
import sys
from pushover import Client

PUSHOVER_USER   = ''
PUSHOVER_APP    = ''
KEY             = ''
CLIENT_ID       = ''
CLIENT_SECRET   = ''
USERNAME        = ''
PASSWORD        = ''

totp = pyotp.TOTP(KEY)

class RedditNotifications:

    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            # set this to just PASSWORD if you don't use 2FA
            password=PASSWORD + ":" + totp.now(),
            user_agent="APP",
            username=USERNAME
        )

        homedir = pwd.getpwuid(os.getuid()).pw_dir
        self.datafile = f"{homedir}/.reddit_seen"

        if os.path.exists(self.datafile):
            self.seen = json.loads(open(self.datafile).read())
        else:
            self.seen = {
                'message': {},
                'comment': {}
            }

        self.pushover = Client(PUSHOVER_USER, api_token=PUSHOVER_APP)


    def main(self):
        for i in range(0, 3):
            try:
                for item in self.reddit.inbox.all():
                    if type(item) == praw.models.reddit.comment.Comment:
                        if item.id in self.seen['comment']:
                            continue

                        self.handle_comment(item)
                    elif type(item) == praw.models.reddit.message.Message:
                        if item.id in self.seen['message']:
                            continue

                        self.handle_message(item)
                    else:
                        raise Exception("unknown item type: %s" % (type(item)))
                break
            except prawcore.exceptions.OAuthException:
                time.sleep(1)


    def handle_comment(self, item):
        url = 'apollo://reddit.com' + item.context

        self.pushover.send_message(item.body, title=item.submission.title, url=url)

        self.seen['comment'][item.id] = 1
        self.save()


    def handle_message(self, item):
        url = 'apollo://reddit.com/message/inbox/'

        self.pushover.send_message(item.body, title=item.subject, url=url)

        self.seen['message'][item.id] = 1
        self.save()


    def save(self):
        with open(self.datafile + '.new','w') as f:
            f.write(json.dumps(self.seen,indent=4))

        os.rename(self.datafile + '.new', self.datafile)


r = RedditNotifications()
r.main()
