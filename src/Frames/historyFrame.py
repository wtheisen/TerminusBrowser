import urwid, time, re

from functools import partial

from debug import DEBUG

class HistoryFrame(urwid.WidgetWrap):
    HistoryFrameFactory = lambda x: HistoryFrame(*x)

    def __init__(self, urwidViewManager, uFilter = None):
        self.uvm = urwidViewManager
        self.uFilter = uFilter


        self.startTime = time.time()
        self.contents = self.buildFrame()
        urwid.WidgetWrap.__init__(self, self.contents)

        self.endTime = time.time()

        self.headerString = f'commandChan: History'
        self.footerStringRight = f'Parsed {self.parsedItems} items in {(self.endTime - self.startTime):.4f}s'

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