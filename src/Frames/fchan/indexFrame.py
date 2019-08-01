import urwid, time

from debug import DEBUG

class IndexFrame(urwid.WidgetWrap):
    IndexFrameFactory = lambda x: IndexFrame(*x)

    def __init__(self, urwidViewManager, uFilter=None):
        self.uvm = urwidViewManager
        self.uFilter = uFilter
        self.headerString = 'CommandChan'

        self.parsedItems = 0
        self.startTime = time.time()
        self.contents = self.buildFrame()
        self.endTime = time.time()

        self.footerStringRight = f'Parsed {self.parsedItems} items in {(self.endTime - self.startTime):.4f}s'

        DEBUG(self.uvm.history)

        urwid.WidgetWrap.__init__(self, self.contents)

    def buildFrame(self):
        boardButtons = []
        for board in self.uvm.currFocusView.boardList:
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
