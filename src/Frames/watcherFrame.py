import urwid, time, re, requests

from functools import partial

from Frames.abstractFrame import AbstractFrame

import logging
log = logging.getLogger(__name__)

class WatcherFrame(AbstractFrame):
    def __init__(self, urwidViewManager, uFilter = None):
        super().__init__(urwidViewManager, uFilter)
        self.load()
        self.headerString = f'commandChan: Watcher'
        self.uFilter = uFilter

    def loader(self):
        self.contents = self.buildFrame()

    def buildFrame(self):
        listbox = self.buildThread()
        return urwid.Pile([listbox])

    def buildThread(self):
        watcherWidgetList = []
        self.uvm.watcherUpdate(None, None)
        for wT, wTDict in self.uvm.watched.items():
            wInfo = urwid.Text(f"Board: {wTDict['board']} -- {wTDict['op']} | Unread: {wTDict['numReplies']}")
            wButton = urwid.Button(f'View thread: {wT}', self.viewThread)
            watcherWidgetList.append(urwid.LineBox(urwid.Pile([wInfo, urwid.Divider('-'), wButton])))

        self.parsedItems = len(watcherWidgetList)

        listbox_content = watcherWidgetList
        listbox = urwid.ListBox(urwid.SimpleListWalker(listbox_content))

        return listbox

    def viewThread(self, button):
        from commandHandlerClass import CommandHandler
        ch = CommandHandler(self.uvm)

        url = button.get_label().split(':')[2]
        items = url.split('/')
        log.debug(items)

        ch.routeCommand('thread' + ' /' + items[3] + '/ ' + items[5].split('.')[0])
