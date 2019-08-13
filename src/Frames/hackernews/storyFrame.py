import urwid, re, time, collections, requests
from debug import DEBUG
from customeTypes import STICKIES
from Frames.abstractFrame import AbstractFrame

class StoryFrame(AbstractFrame):
    def __init__(self, story, urwidViewManager, uFilter=None):
        super().__init__(urwidViewManager, uFilter)
        self.story = story

        self.base = 'https://hacker-news.firebaseio.com/v0/'
        self.url = self.base + self.story + '.json'

        self.headers = {
            'user-agent': 'hackernews-TerminusBrowse'
        }
        self.info_text = 'Score: {} Comments: {}'

        self.load()
        self.headerString = f'TerminusBrowse: {self.story}'

    # Overrides super
    def loader(self):
        self.titles = self.getJSONCatalog(self.url)
        self.contents = urwid.Pile(self.buildFrame(self.story))

    def buildFrame(self, board):
        '''returns the board widget'''

        threadButtonList = []

        for title, threadInfo in self.titles.items():
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

        return self.parseStoryBoard(data)

    def parseStoryBoard(self, data):
        titles = collections.OrderedDict()

        for story in data[1:10]:
            storyData = requests.get(self.base + 'item/' + str(story) + '.json').json()
            # Need to research this
            # inconsistent returned data - sometimes throws a key error
            try:
                titles[storyData['title']] = (  storyData['id'],
                                                storyData['score'],
                                                storyData['descendants'])
            except:
                pass


        return titles

    def changeFrameThread(self, button):
        from commandHandlerClass import CommandHandler
        ch = CommandHandler(self.uvm)
        ch.routeCommand('hnp ' + self.story + ' ' + button.get_label())

    def changeSubPage(self, button):
        from commandHandlerClass import CommandHandler
        ch = CommandHandler(self.uvm)
        ch.routeCommand('story ' + self.story + ' ' + button.get_label())
