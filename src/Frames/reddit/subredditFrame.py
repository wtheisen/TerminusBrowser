import urwid, re, time, collections, requests
from debug import DEBUG
from customeTypes import STICKIES
from Frames.abstractFrame import AbstractFrame

class SubredditFrame(AbstractFrame):    
    def __init__(self, subreddit, token, urwidViewManager, uFilter=None):
        super().__init__(urwidViewManager, uFilter)
        self.subreddit = '/r/' + subreddit if not subreddit.startswith('/r/') else subreddit

        self.url = 'https://www.reddit.com' + self.subreddit + '.json' + '?limit=100'
        self.token = token
        if self.token:
            self.url += '&after=' + self.token

        self.headers = {
            'user-agent': 'reddit-TerminusBrowse'
        }
        self.info_text = 'Upvotes: {} Comments: {}'

        self.load()
        self.headerString = f'TerminusBrowse: {self.subreddit}'

    # Overrides super
    def loader(self):
        self.titles = self.getJSONCatalog(self.url)
        self.contents = urwid.Pile(self.buildFrame(self.subreddit))

    def buildFrame(self, board):
        '''returns the board widget'''

        threadButtonList = []

        for title, threadInfo in self.titles.items():
            if title == 'Next':
                if not self.uFilter:
                    subButton = urwid.Button(str(threadInfo[0]), self.changeSubPage)
                    threadButtonList.append(urwid.LineBox(urwid.Pile([subButton, urwid.Divider('-'), urwid.Text(threadInfo[1])])))
                continue
            title = title.replace('-', ' ')
            if self.uFilter:
                if re.search(self.uFilter.lower(), title.lower()):
                    threadButton = urwid.Button(str(threadInfo[0]), self.changeFrameThread)
                    threadInfo = urwid.Text(self.info_text.format(str(threadInfo[1]),str(threadInfo[2])))
                    threadList = [threadButton, urwid.Divider('-'), urwid.Divider(), urwid.Text(title), urwid.Divider(), urwid.Divider('-'), threadInfo]
                    threadButtonList.append(urwid.LineBox(urwid.Pile(threadList)))
            else:
                threadButton = urwid.Button(str(threadInfo[0]), self.changeFrameThread)
                threadInfo = urwid.Text(self.info_text.format(str(threadInfo[1]), str(threadInfo[2])))
                threadList = [threadButton, urwid.Divider('-'), urwid.Divider(), urwid.Text(title), urwid.Divider(), urwid.Divider('-'), threadInfo]
                threadButtonList.append(urwid.LineBox(urwid.Pile(threadList)))

        self.parsedItems = len(threadButtonList)
        catalogueButtons = urwid.GridFlow(threadButtonList, 30, 2, 2, 'center')
        listbox = urwid.ListBox(urwid.SimpleListWalker([catalogueButtons]))

        self.uvm.itemCount = len(threadButtonList)
        return [listbox]

    def getJSONCatalog(self, url):
        response = requests.get(url, headers=self.headers)

        data = response.json()

        return self.parseSubreddit(data)

    def parseSubreddit(self, data):
        titles = collections.OrderedDict()
        posts = data['data']['children']

        DEBUG(posts)

        for post in posts:
            if self.uvm.stickies == STICKIES.HIDE and post['data']['stickied']:
                continue

            titles[post['data']['title']] = (post['data']['permalink'],
                                             post['data']['score'],
                                             post['data']['num_comments'])

        # parse next key
        if data['data']['after']:
            titles['Next'] = (data['data']['after'],
                             'Next',
                             '')

        return titles

    def changeFrameThread(self, button):
        from commandHandlerClass import CommandHandler
        ch = CommandHandler(self.uvm)
        ch.routeCommand('post ' + self.subreddit + ' ' + button.get_label())

    def changeSubPage(self, button):
        from commandHandlerClass import CommandHandler
        ch = CommandHandler(self.uvm)
        ch.routeCommand('sub ' + self.subreddit + ' ' + button.get_label())
