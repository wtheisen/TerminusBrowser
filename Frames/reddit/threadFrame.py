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
                item['data']['author'],
                item['data']['body'],
                item['data']['created'],
                score=item['data']['score'],
                replies=self.get_replies(item)
            ))
            self.parsedItems += 1
        
        tree = Post(
            item['data']['author'],
            self.get_post(post),
            item['data']['created'],
            score=item['data']['score'],
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
                        item['data']['author'],
                        item['data']['body'],
                        item['data']['created'],
                        score=item['data']['score'],
                        replies=self.get_replies(item)
                    ))
                    self.parsedItems += 1
        return my_children

    
class CommentWidget(urwid.TreeWidget):
    unexpanded_icon = urwid.AttrMap(urwid.TreeWidget.unexpanded_icon,
        'dirmark')
    expanded_icon = urwid.AttrMap(urwid.TreeWidget.expanded_icon,
        'dirmark')

    def __init__(self, node):
        self._innerwidget = None
        self.info_text = 'score: {} user: {}'

        self.__super.__init__(node)
        
        self._has_child = self.get_node().get_value().replies != []
        self.expanded = (self.get_node().get_depth() < 3 or
                         not self._has_child)
        self.update_expanded_icon()

    def get_inner_widget(self):
        if self._innerwidget is None:
            self._innerwidget = self.load_inner_widget()
        return self._innerwidget

    def load_inner_widget(self):
        content = [urwid.Text(self.get_display_text()), urwid.Divider('-'),
                   urwid.Text(self.get_info_text())]
        return urwid.LineBox(urwid.Pile(content))

    def keypress(self, size, key):
        """allow subclasses to intercept keystrokes"""
        if key == 'right' and self._has_child:
            self.expanded = not self.expanded
            self.update_expanded_icon()
        else:
            key = self.__super.keypress(size, key)
        return key

    def get_display_text(self):
        return self.get_node().get_value().content

    def get_info_text(self):
        return self.info_text.format(self.get_node().get_value().score,
                                     self.get_node().get_value().userIden)


class CommentNode(urwid.ParentNode):
    """ Data storage object for interior/parent nodes """
    def load_widget(self):
        return CommentWidget(self)

    def load_child_keys(self):
        data = self.get_value()
        return range(len(data.replies))

    def load_child_node(self, key):
        """Return either an ExampleNode or ExampleParentNode"""
        childdata = self.get_value().replies[key]
        childdepth = self.get_depth() + 1
        childclass = CommentNode
        return childclass(childdata, parent=self, key=key, depth=childdepth)
