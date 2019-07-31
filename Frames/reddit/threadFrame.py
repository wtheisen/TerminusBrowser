import urwid, time, requests, re

from debug import DEBUG
from postClass import Post
from customUrwidClasses import QuoteButton

class RedditThreadFrame(urwid.WidgetWrap):
    def __init__(self, subString, threadUri, urwidViewManager, uFilter = None):
        self.uvm = urwidViewManager
        self.subString = subString
        self.threadUri = threadUri
        self.uFilter = uFilter

        self.url = 'https://www.reddit.com' + self.threadUri
        self.imageUrl = None
        self.headers = {
            'user-agent': 'reddit-commandChan'        
        }

        self.postReplyDict = {}

        self.startTime = time.time()
        self.comments = self.getJSONThread()
        self.contents = self.buildFrame()
        urwid.WidgetWrap.__init__(self, self.contents)

        self.endTime = time.time()

    def getJSONThread(self):
        response = requests.get(self.url + '.json', headers=self.headers)
        data = response.json()
        return self.parseRedditThread(data)

    def parseRedditThread(self, data):
        post     = data[0]['data']['children'][0]
        comments = data[1]['data']['children']
        children  = []
        for item in comments:
            children.append({
                'name': item['data'].get('body', ''),
                'children': self.get_replies(item)
            })
        
        tree = {'name': self.get_post(post), 'children': children}
        return tree

    def buildFrame(self):
        topnode = ParentCommentNode(self.comments)
        return urwid.TreeListBox(urwid.TreeWalker(topnode))

    def get_post(self, post):
        return "{}\n{}".format(post['data']['title'], post['data']['selftext'] if post['data']['selftext'] else post['data']['url'])

    def get_replies(self, comment):
        my_children = []

        replies = comment['data'].get('replies', None)
        if replies:
            for item in replies['data']['children']:
                if item['data'].get('body'):
                    my_children.append({'name': item['data']['body'], 'children': self.get_replies(item)})

        return my_children

    
class CommentWidget(urwid.TreeWidget):
    unexpanded_icon = urwid.AttrMap(urwid.TreeWidget.unexpanded_icon,
        'dirmark')
    expanded_icon = urwid.AttrMap(urwid.TreeWidget.expanded_icon,
        'dirmark')

    def __init__(self, node):
        self._innerwidget = urwid.Text("test")
        self.__super.__init__(node)
        self.expanded = self.get_node().get_depth() < 3
        self.update_expanded_icon()

    def keypress(self, size, key):
        """allow subclasses to intercept keystrokes"""
        if key == 'right':
            self.expanded = not self.expanded
            self.update_expanded_icon()
        else:
            key = self.__super.keypress(size, key)
        return key

    def get_display_text(self):
        return self.get_node().get_value()['name']

class LeafCommentWidget(urwid.TreeWidget):
    """ Display widget for leaf nodes """
    unexpanded_icon = urwid.AttrMap(urwid.TreeWidget.unexpanded_icon,
        'dirmark')
    expanded_icon = urwid.AttrMap(urwid.TreeWidget.expanded_icon,
        'dirmark')

    def get_display_text(self):
        return self.get_node().get_value()['name']


class LeafNode(urwid.TreeNode):
    """ Data storage object for leaf nodes """
    def load_widget(self):
        return LeafCommentWidget(self)


class ParentCommentNode(urwid.ParentNode):
    """ Data storage object for interior/parent nodes """
    def load_widget(self):
        return CommentWidget(self)

    def load_child_keys(self):
        data = self.get_value()
        return range(len(data['children']))

    def load_child_node(self, key):
        """Return either an ExampleNode or ExampleParentNode"""
        childdata = self.get_value()['children'][key]
        childdepth = self.get_depth() + 1
        if len(childdata['children']):
            childclass = ParentCommentNode
        else:
            childclass = LeafNode
        return childclass(childdata, parent=self, key=key, depth=childdepth)
