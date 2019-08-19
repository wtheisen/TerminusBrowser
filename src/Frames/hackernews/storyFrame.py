import urwid, re, time, collections, requests
from customeTypes import STICKIES
from Frames.abstractFrame import AbstractFrame
import time

import logging
log = logging.getLogger(__name__)

class StoryFrame(AbstractFrame):
    def __init__(self, story, page, urwidViewManager, uFilter=None):
        super().__init__(urwidViewManager, uFilter)
        self.story = story
        self.page = page

        storyDict = {
            'top': 'front_page',
            'new': 'story',
            'ask': 'ask_hn',
            'show': 'show_hn',
            'jobs' : 'job'
        }

        # 'search' will search by relevancy and score
        # this only works well w this api for front page posts
        # using 'search' for say, 'job' will return posts from too long ago
        search = 'search' if self.story == 'top' else 'search_by_date'
        self.url = f'https://hn.algolia.com/api/v1/{search}?tags=' + storyDict[self.story] + f'&page={self.page}'

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
            if title == 'Next':
                if not self.uFilter:
                    subButton = urwid.Button(str(threadInfo[0]), self.changeStoryPage)
                    threadButtonList.append(urwid.LineBox(urwid.Pile([subButton, urwid.Divider('-'), urwid.Text(threadInfo[1])])))
                continue
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

        for i in range(len(data['hits'])):
            titles[data['hits'][i]['title']] = (data['hits'][i]['objectID'],
                                            data['hits'][i]['points'],
                                            data['hits'][i]['num_comments'])

        if int(self.page) < data['nbPages'] - 1:
            titles['Next'] = (int(self.page) + 1,
                            'Next',
                            '')

        return titles

    def changeFrameThread(self, button):
        from commandHandlerClass import CommandHandler
        ch = CommandHandler(self.uvm)
        ch.routeCommand('hnp ' + self.story + ' ' + button.get_label())

    def changeStoryPage(self, button):
        from commandHandlerClass import CommandHandler
        ch = CommandHandler(self.uvm)
        ch.routeCommand('story ' + self.story + ' ' + button.get_label())
