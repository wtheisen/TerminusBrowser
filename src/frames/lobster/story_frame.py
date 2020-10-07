import urwid, re, time, collections, requests
from customer_types import STICKIES
from frames.abstract_frame import AbstractFrame
import time

import logging
log = logging.getLogger(__name__)

class StoryFrame(AbstractFrame):
    def __init__(self, story, page, urwidViewManager, uFilter=None):
        super().__init__(urwidViewManager, uFilter)
        self.story = story
        self.page = page

        self.story = None
        # 'search' will search by relevancy and score
        # this only works well w this api for front page posts
        # using 'search' for say, 'job' will return posts from too long ago
        search = 'search' if self.story == 'top' else 'search_by_date'
        if self.story:
            self.url = f'https://lobste.rs/{self.story}/page/{page}.json'
        else:
            self.url = f'https://lobste.rs/page/{page}.json'

        self.headers = {
            'user-agent': 'lobster-TerminusBrowser'
        }
        self.info_text = 'Score: {} Comments: {}'

        self.load()
        self.headerString = f'TerminusBrowser: {self.story}'

    # Overrides super
    def loader(self):
        self.titles = self.getJSONCatalog(self.url)
        self.contents = urwid.Pile(self.buildFrame(self.story))

    def buildFrame(self, board):
        '''returns the board widget'''

        threadButtonList = []

        for title, l, s, c, t  in self.titles.items():
            if self.uFilter:
                if re.search(self.uFilter.lower(), title.lower()):
                    threadButton = urwid.Button(str(l), self.changeFrameThread)
                    threadInfo = urwid.Text(self.info_text.format(str(s),str(c)))
                    threadList = [threadButton, urwid.Divider('-'), urwid.Divider(), urwid.Text(title), urwid.Divider(), urwid.Divider('-'), threadInfo]
                    threadButtonList.append(urwid.LineBox(urwid.Pile(threadList)))
            else:
                threadButton = urwid.Button(str(l), self.changeFrameThread)
                threadInfo = urwid.Text(self.info_text.format(str(s),str(c)))
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
        titles = []

        for p in data:
            titles.append((p['title'], p['comments_url'], p['score'], p['comments'], p['created_at']))

        return titles

    def changeFrameThread(self, button):
        from command_handler_class import CommandHandler
        ch = CommandHandler(self.uvm)
        ch.routeCommand('hnp ' + self.story + ' ' + button.get_label())

    def changeStoryPage(self, button):
        from command_handler_class import CommandHandler
        ch = CommandHandler(self.uvm)
        ch.routeCommand('story ' + self.story + ' ' + button.get_label())
