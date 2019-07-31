import urwid, re, time, collections, requests
from customeTypes import STICKIES

class SubredditFrame(urwid.WidgetWrap):
    def __init__(self, boardString, urwidViewManager, uFilter=None):
        self.uvm = urwidViewManager
        self.boardString = boardString
        self.uFilter = uFilter

        self.url = 'https://www.reddit.com' + self.boardString + '.json'
        self.headers = {
            'user-agent': 'reddit-commandChan'
        }
        self.threadNums = []
        self.info_text = 'Replies: {} Images: {}'
        self.parsedItems = 0

        self.startTime = time.time()

        self.titles = self.getJSONCatalog(self.url)
        self.contents = urwid.Pile(self.buildFrame(boardString))
        urwid.WidgetWrap.__init__(self, self.contents)
        self.endTime = time.time()
        self.footerStringRight = f'Parsed {self.parsedItems} items in {(self.endTime - self.startTime):.4f}s'

    def buildFrame(self, board):
        '''returns the board widget'''

        threadButtonList = []

        for title, threadInfo in self.titles.items():
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

        for post in posts:
            if self.uvm.stickies == STICKIES.HIDE and post['data']['stickied']:
                continue

            titles[post['data']['title']] = (post['data']['permalink'],
                                             post['data']['score'],
                                             post['data']['subreddit'])
            self.threadNums.append(post['data']['title'])

        return titles

    def changeFrameThread(self, button):
        from commandHandlerClass import CommandHandler
        ch = CommandHandler(self.uvm)
        ch.routeCommand('post ' + self.boardString + ' ' + button.get_label())
