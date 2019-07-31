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
        topnode = CommentNode(self.comments)
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
        self._innerwidget = None
        self.__super.__init__(node)
        self.expanded = self.get_node().get_depth() < 3 or not self.get_node().get_value()['children']
        self.update_expanded_icon()

    def get_inner_widget(self):
        if self._innerwidget is None:
            self._innerwidget = self.load_inner_widget()
        return self._innerwidget

    def load_inner_widget(self):
        return urwid.LineBox(urwid.Text(self.get_display_text()))

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


class CommentNode(urwid.ParentNode):
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
        childclass = CommentNode
        return childclass(childdata, parent=self, key=key, depth=childdepth)
