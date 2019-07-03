#Board view classes
import time, urwid, re
from viewStyles import VIEWSTYLES
from threadClass import displayThread

def buildView(style, board, titles, userFilter, indexView):
    if style is VIEWSTYLES.BOXES:
        return urwidBoardViewBoxes(board, titles, userFilter, indexView)

class urwidBoardViewBoxes:
    def __init__(self, board, titles, userFilter, indexView):
        self.board = board
        self.titles = titles
        self.userFilter = userFilter
        self.indexView = indexView

        self.itemCount = 0

        self.frame = None

        self.buildHeaderView()
        self.createBoardView()

    def buildHeaderView(self):
        self.header = urwid.AttrWrap(urwid.Text('CommandChan'), 'header')

    def createBoardCatalogueView(self):
        '''returns the board widget'''

        threadButtonList = []

        for title, threadInfo in self.titles.items():
            title = title.replace('-', ' ')
            if self.userFilter:
                if re.search(userFilter, title):
                    threadButton = urwid.Button(str(threadInfo[0]), displayThread)
                    threadInfo = urwid.Text('Replies: ' + str(threadInfo[1]) + ' Images: ' + str(threadInfo[2]))
                    threadList = [threadButton, urwid.Divider('-'), urwid.Divider(), urwid.Text(title), urwid.Divider(), urwid.Divider('-'), threadInfo]
                    threadButtonList.append(urwid.LineBox(urwid.Pile(threadList)))
            else:
                threadButton = urwid.Button(str(threadInfo[0]), displayThread)
                threadInfo = urwid.Text('Replies: ' + str(threadInfo[1]) + ' Images: ' + str(threadInfo[2]))
                threadList = [threadButton, urwid.Divider('-'), urwid.Divider(), urwid.Text(title), urwid.Divider(), urwid.Divider('-'), threadInfo]
                threadButtonList.append(urwid.LineBox(urwid.Pile(threadList)))

        catalogueButtons = urwid.GridFlow(threadButtonList, 30, 2, 2, 'center')
        listbox = urwid.ListBox(urwid.SimpleListWalker([catalogueButtons]))

        self.itemCount = len(threadButtonList)
        return listbox

    def createBoardView(self):
        catalogueBox = self.createBoardCatalogueView()
        view = urwid.LineBox(urwid.Pile([catalogueBox]))
        catalogue = urwid.Overlay(view, self.indexView, 'center', ('relative', 90), 'middle', ('relative', 95))
        self.frame = urwid.Frame(urwid.AttrWrap(catalogue, 'body'), header=self.header)
