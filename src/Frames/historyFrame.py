import urwid, time, re

from functools import partial

from debug import DEBUG
from abstractFrame import AbstractFrame

class HistoryFrame(AbstractFrame):
    def __init__(self, urwidViewManager, uFilter = None):
        super().__init__(urwidViewManager, uFilter)
        self.load()
        self.headerString = f'commandChan: History'

    def loader(self):
        self.contents = self.buildFrame()
        
    def buildFrame(self):
        listbox = self.buildThread()
        return urwid.Pile([listbox])

    def buildThread(self):
        historyWidgetList = []
        for h in self.uvm.history:
            frame = h[0]
            factory = h[1]
            args = h[2]

            if self.uFilter:
                if self.uFilter in args:
                    hInfo = urwid.Text(f'Frame: {frame}, Info: {args}')
                    hButton = urwid.Button(f'{self.uvm.history.index(h)}: Restore', self.restore)
                    historyWidgetList.append(urwid.LineBox(urwid.Pile([hInfo, urwid.Divider('-'), hButton])))
            else:
                hInfo = urwid.Text(f'Frame: {frame}, Info: {args}')
                hButton = urwid.Button(f'{self.uvm.history.index(h)}: Restore', self.restore)
                historyWidgetList.append(urwid.LineBox(urwid.Pile([hInfo, urwid.Divider('-'), hButton])))

        self.parsedItems = len(historyWidgetList)

        listbox_content = historyWidgetList
        listbox = urwid.ListBox(urwid.SimpleListWalker(listbox_content))

        return listbox

    def restore(self, button):
        from commandHandlerClass import CommandHandler
        ch = CommandHandler(self.uvm)
        ch.routeCommand('history ' + button.get_label()[0])
