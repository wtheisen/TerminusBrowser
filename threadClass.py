#Thread Class
import requests, json, collections, re
import urwid

from debug import DEBUG
from postClass import Post
from threadViewClasses import buildView
from customeTypes import VIEWSTYLES, SITE

class Thread:
    def __init__(self, urwidViewManager):
        self.uvm = urwidViewManager

        if self.uvm.site == SITE.FCHAN:
            self.url = 'https://a.4cdn.org' + self.uvm.boardString + 'thread/' + str(self.uvm.threadID)
            self.imageUrl = 'http://boards.4chan.org' + self.uvm.boardString + 'thread/' + str(self.uvm.threadID)
            self.headers = {}
        elif self.uvm.site == SITE.REDDIT:
            self.url = 'https://www.reddit.com' + str(self.uvm.threadID)
            self.headers = {
                'user-agent': 'reddit-commandChan'
            }
        self.postReplyDict = {}

        self.comments = self.getJSONThread()

        buildView(VIEWSTYLES.BOXES, self.uvm, self)


    def getJSONThread(self):
        response = requests.get(self.url + '.json', headers=self.headers)
        data = response.json()
        if self.uvm.site == SITE.FCHAN:
            return self.parseFourThread(data)
        elif self.uvm.site == SITE.REDDIT:
            return self.parseRedditThread(data)
        return collections.OrderedDict()

    def parseFourThread(self, data):
        commentObjList = []
        posts = data["posts"]

        for post in posts:
            if str(post["resto"]) == '0':
                self.currentThreadOPNumber = str(post["no"])

            p = Post(
                str(post["no"]),
                post["com"] if 'com' in post else "",
                post["now"],
                'https://i.4cdn.org' + self.uvm.boardString + str(post["tim"]) + post["ext"] if 'ext' in post else ''
            )

            commentObjList.append(p)

        return commentObjList

    def parseRedditThread(self, data):
        top_level_comments = collections.OrderedDict()
        post     = data[0]['data']['children'][0]
        comments = data[1]['data']['children']

        self.postReplyDict['OP'] = []
        # add post's content first
        if post['data'].get('post_hint') == 'image':
            top_level_comments[('OP', post['data']['permalink'])] = (post['data']['title'], post['data']['url'])
        elif post['data'].get('post_hint') == 'link':
            top_level_comments[('OP', post['data']['permalink'])] = (post['data']['title'], post['data']['url'])
        else:
            top_level_comments[('OP', post['data']['permalink'])] = (post['data']['selftext'], '')

        for comment in comments:
            if comment['kind'] == 'more':
                # TODO: PAGINATE
                break

            self.postReplyDict[comment['data']['author']] = []
            top_level_comments[(comment['data']['author'], comment['data']['permalink'])] = (comment['data']['body'], comment['data']['permalink'])

        return top_level_comments