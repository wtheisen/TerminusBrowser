import urwid, time, requests, re
from html2text import html2text

from debug import DEBUG
from postClass import Post
from customUrwidClasses import QuoteButton
from Views.treeThreadClasses import CommentNode
from Frames.abstractFrame import AbstractFrame

class HackerNewsThreadFrame(AbstractFrame):
    def __init__(self, story, threadUri, urwidViewManager, uFilter = None):
        super().__init__(urwidViewManager, uFilter)
        self.story = story
        self.threadUri = threadUri

        # unofficial HN api, more dev friendly json response
        self.url = 'https://hn.algolia.com/api/v1/items/' + str(threadUri)
        self.headers = {
            'user-agent': 'hackernews-commandChan'
        }

        self.load()
        self.headerString = f'commandChan: {self.story} -- {threadUri}'

    # Overrides super
    def loader(self):
        self.comments = self.getJSONThread()
        self.contents = self.buildFrame()

    def getJSONThread(self):
        response = requests.get(self.url + '.json', headers=self.headers)
        data = response.json()
        return self.parseHNThread(data)

    def parseHNThread(self, data):
        post     = data
        comments = data['children']
        children  = []
        # b/c the way posts are "different" than comments
        # have to load replies for each top level comment
        # then add as child to post
        for item in comments:
            if not item['text']:
                continue

            children.append(Post(
                item['author'],
                # text is returned as raw html
                html2text(item['text']).replace('\n', ' '),
                item['created_at'],
                score=0, # HN hides comment scores
                replies=self.get_replies(item)
            ))
            self.parsedItems += 1

        tree = Post(
            data['author'], # author
            self.get_post(post),
            post['created_at'],
            score=post['points'],
            replies=children
        )
        return tree

    def buildFrame(self):
        topnode = CommentNode(self.comments)
        return urwid.TreeListBox(urwid.TreeWalker(topnode))

    def get_post(self, post):
        return "{}\n{}".format(post['title'],
                               post['url'])

    def get_replies(self, comment):
        my_children = []

        replies = comment['children']
        if replies:
            for item in replies:
                if item['text']:
                    my_children.append(Post(
                        item['author'],
                        html2text(item['text']).replace('\n', ' '),
                        item['created_at'],
                        score=0, # HN hides comment scores
                        replies=self.get_replies(item)
                    ))
                    self.parsedItems += 1
        return my_children
