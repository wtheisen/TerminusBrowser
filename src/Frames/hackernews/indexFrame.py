import urwid, time
from customeTypes import SITE

from Frames.abstractFrame import AbstractFrame

import logging
log = logging.getLogger(__name__)

class HackerNewsIndexFrame(AbstractFrame):
    def __init__(self, urwidViewManager, uFilter=None):
        super().__init__(urwidViewManager, uFilter)
        self.headerString = 'TerminusBrowse'

        self.storyList = self.uvm.cfg.deep_get(SITE.HACKERNEWS, 'stories')

        self.load()

    # Overrides super
    def loader(self):
        self.contents = self.buildFrame()

    def buildFrame(self):
        boardButtons = []
        for story in self.storyList:
            if self.uFilter:
                if self.uFilter.lower() in story.lower():
                    boardButtons.append(urwid.LineBox(urwid.AttrWrap(urwid.Button(story, self.changeFrameBoard), 'center')))
            else:
                boardButtons.append(urwid.LineBox(urwid.AttrWrap(urwid.Button(story, self.changeFrameBoard), 'center')))

        self.parsedItems = len(boardButtons)
        width = len(max(self.storyList, key=len))
        buttonGrid = urwid.GridFlow(boardButtons, width + 9, 2, 2, 'center') # add 9 to width to account for widget padding
        listbox_content = [buttonGrid]

        return urwid.ListBox(urwid.SimpleListWalker(listbox_content))

    def changeFrameBoard(self, button):
        from commandHandlerClass import CommandHandler
        ch = CommandHandler(self.uvm)
        ch.routeCommand('story ' + button.get_label() + ' ' +  '0')
