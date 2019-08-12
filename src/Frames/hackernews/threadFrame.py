import urwid, time, requests, re

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

        self.url = 'https://hacker-news.firebaseio.com/v0/item/' + str(threadUri)
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
        return self.parseRedditThread(data)

    def parseRedditThread(self, data):
        post     = data
        '''
        comments = data[1]['data']['children']
        children  = []
        # b/c the way posts are "different" than comments
        # have to load replies for each top level comment
        # then add as child to post
        for item in comments:
            if not item['data'].get('body'):
                continue
            
            children.append(Post(
                item['data'].get('author'),
                item['data'].get('body'),
                item['data'].get('created'),
                score=item['data'].get('score'),
                replies=self.get_replies(item)
            ))
            self.parsedItems += 1
            '''
        
        DEBUG(post)
        tree = Post(
            post['by'], # author
            self.get_post(post),
            post['time'],
            score=post['score'],
            replies=[Post('t','e','s','t','yo')]
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

        replies = comment['data'].get('replies', None)
        if replies:
            for item in replies['data']['children']:
                if item['data'].get('body'):
                    my_children.append(Post(
                        item['data'].get('author'),
                        item['data'].get('body'),
                        item['data'].get('created'),
                        score=item['data'].get('score'),
                        replies=self.get_replies(item)
                    ))
                    self.parsedItems += 1
        return my_children
