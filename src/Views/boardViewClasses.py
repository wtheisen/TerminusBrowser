#Board view classes
import time, urwid, re
from customeTypes import VIEWSTYLES, SITE

def buildView(style, urwidViewManager, board):
    if style is VIEWSTYLES.BOXES:
        return urwidBoardViewBoxes(urwidViewManager, board)

class urwidBoardViewBoxes:
    def __init__(self, urwidViewManager, board):
        self.uvm = urwidViewManager
        self.b = board

        self.itemCount = 0


        self.info_text = '{} {}'
        if self.uvm.site == SITE.FCHAN:
            self.info_text = 'Replies: {} Images: {}'
        elif self.uvm.site == SITE.REDDIT:
            self.info_text = 'Replies: {} Subreddit: {}'

        self.buildHeaderView()
        self.buildBoardView()
        #self.uvm.frame = self.frame

    def buildHeaderView(self):
        self.header = urwid.AttrWrap(urwid.Text('CommandChan'), 'header')

    def createBoardCatalogueView(self):
        '''returns the board widget'''

        threadButtonList = []

        for title, threadInfo in self.b.titles.items():
            title = title.replace('-', ' ')
            if self.uvm.userFilter:
                if re.search(self.uvm.userFilter.lower(), title.lower()):
                    threadButton = urwid.Button(str(threadInfo[0]), self.uvm.displayThread)
                    threadInfo = urwid.Text(self.info_text.format(str(threadInfo[1]),str(threadInfo[2])))
                    threadList = [threadButton, urwid.Divider('-'), urwid.Divider(), urwid.Text(title), urwid.Divider(), urwid.Divider('-'), threadInfo]
                    threadButtonList.append(urwid.LineBox(urwid.Pile(threadList)))
            else:
                threadButton = urwid.Button(str(threadInfo[0]), self.uvm.displayThread)
                threadInfo = urwid.Text(self.info_text.format(str(threadInfo[1]), str(threadInfo[2])))
                threadList = [threadButton, urwid.Divider('-'), urwid.Divider(), urwid.Text(title), urwid.Divider(), urwid.Divider('-'), threadInfo]
                threadButtonList.append(urwid.LineBox(urwid.Pile(threadList)))

        catalogueButtons = urwid.GridFlow(threadButtonList, 30, 2, 2, 'center')
        listbox = urwid.ListBox(urwid.SimpleListWalker([catalogueButtons]))

        self.uvm.itemCount = len(threadButtonList)
        return listbox

    def buildBoardView(self):
        catalogueBox = self.createBoardCatalogueView()
        view = urwid.LineBox(urwid.Pile([catalogueBox]))
        # catalogue = urwid.Overlay(view, self.uvm.indexView, 'center', ('relative', 90), 'middle', ('relative', 95))
        self.uvm.bodyView = urwid.Overlay(view, self.uvm.indexView, 'center', ('relative', 90), 'middle', ('relative', 95))
        # self.uvm.bodyView = urwid.Frame(urwid.AttrWrap(catalogue, 'body'), header=self.header)
