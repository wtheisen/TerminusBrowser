import urwid, time
from debug import DEBUG

from Frames.abstractFrame import AbstractFrame

class RedditIndexFrame(AbstractFrame):
    def __init__(self, urwidViewManager, uFilter=None):
        super().__init__(urwidViewManager, uFilter)
        self.headerString = 'commandChan'

        self.load()
    
    # Overrides super
    def loader(self):
        self.contents = self.buildFrame()

    def buildFrame(self):
        boardButtons = []
        DEBUG(self.uvm.subredditList)
        for subreddit in self.uvm.subredditList:
            if self.uFilter:
                if self.uFilter.lower() in subreddit.lower():
                    boardButtons.append(urwid.LineBox(urwid.AttrWrap(urwid.Button('/r/' + subreddit, self.changeFrameBoard), 'center')))
            else:
                boardButtons.append(urwid.LineBox(urwid.AttrWrap(urwid.Button('/r/' + subreddit, self.changeFrameBoard), 'center')))

        self.parsedItems = len(boardButtons)
        width = len(max(self.uvm.subredditList, key=len))
        buttonGrid = urwid.GridFlow(boardButtons, width + 9, 2, 2, 'center') # add 9 to width to account for widget padding
        listbox_content = [buttonGrid]

        return urwid.ListBox(urwid.SimpleListWalker(listbox_content))

    def changeFrameBoard(self, button):
        from commandHandlerClass import CommandHandler
        ch = CommandHandler(self.uvm)
        ch.routeCommand('subreddit ' + button.get_label())
