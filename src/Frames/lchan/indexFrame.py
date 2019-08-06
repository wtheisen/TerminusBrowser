import urwid, time

from debug import DEBUG
from customeTypes import SITE

from Frames.abstractFrame import AbstractFrame

class IndexFrame(AbstractFrame):
    def __init__(self, urwidViewManager, uFilter=None):
        super().__init__(urwidViewManager, uFilter)

        self.uvm.currFocusView.site = SITE.LCHAN

        self.headerString = 'CommandChan'

        self.boardList = self.uvm.cfg.deep_get(SITE.LCHAN, 'boards')

        self.load()

        DEBUG(self.uvm.history)

    # Overrides super
    def loader(self):
        self.contents = self.buildFrame()

    def buildFrame(self):
        boardButtons = []
        for board in self.boardList:
            if self.uFilter:
                if self.uFilter.lower() in board.lower():
                    boardButtons.append(urwid.LineBox(urwid.AttrWrap(urwid.Button(board, self.changeFrameBoard), 'center')))
            else:
                boardButtons.append(urwid.LineBox(urwid.AttrWrap(urwid.Button(board, self.changeFrameBoard), 'center')))

        self.parsedItems = len(boardButtons)
        buttonGrid = urwid.GridFlow(boardButtons, 12, 2, 2, 'center')
        listbox_content = [buttonGrid]

        return urwid.ListBox(urwid.SimpleListWalker(listbox_content))

    def changeFrameBoard(self, button):
        from commandHandlerClass import CommandHandler
        ch = CommandHandler(self.uvm)
        ch.routeCommand('board ' + button.get_label())

        # commands.board(self.uvm, button.get_label())
