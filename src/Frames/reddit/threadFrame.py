import urwid, time, requests, re

from debug import DEBUG
from postClass import Post
from customUrwidClasses import QuoteButton
from Views.treeThreadClasses import CommentNode

class RedditThreadFrame(urwid.WidgetWrap):
    RedditThreadFrameFactory = lambda x: RedditThreadFrame(*x)

    def __init__(self, subString, threadUri, urwidViewManager, uFilter = None):
        self.uvm = urwidViewManager
        self.subString = subString
        self.threadUri = threadUri
        self.uFilter = uFilter
        self.parsedItems = 0

        self.url = 'https://www.reddit.com' + self.threadUri
        self.headers = {
            'user-agent': 'reddit-commandChan'        
        }

        self.startTime = time.time()
        self.comments = self.getJSONThread()
        self.contents = self.buildFrame()
        urwid.WidgetWrap.__init__(self, self.contents)
        self.endTime = time.time()

        self.headerString = f'commandChan: {self.subString} -- {threadUri.split("/")[-2]}'
        self.footerStringRight = f'Parsed {self.parsedItems} items in {(self.endTime - self.startTime):.4f}s'


    def getJSONThread(self):
        response = requests.get(self.url + '.json', headers=self.headers)
        data = response.json()
        return self.parseRedditThread(data)

    def parseRedditThread(self, data):
        post     = data[0]['data']['children'][0]
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
        
        tree = Post(
            post['data'].get('author'),
            self.get_post(post),
            post['data'].get('created'),
            score=post['data'].get('score'),
            replies=children
        )
        return tree

    def buildFrame(self):
        topnode = CommentNode(self.comments)
        return urwid.TreeListBox(urwid.TreeWalker(topnode))

    def get_post(self, post):
        return "{}\n{}".format(post['data']['title'], 
                               post['data']['selftext'] if post['data']['selftext']
                                                        else post['data']['url'])

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
