import urwid

from viewClass import View

from Frames.indexFrame import IndexFrame
from Frames.boardFrame import BoardFrame
from Frames.threadFrame import ThreadFrame

from customeTypes import LEVEL, MODE, SITE
from debug import DEBUG

def preCommand(uvm):
    uvm.commandBar.set_caption('')
    uvm.mode = MODE.NORMAL
    uvm.body.focus_position = 'body'

def postCommand(uvm):
    uvm.buildAddHeaderView(uvm.currFocusView)
    uvm.buildAddFooterView(uvm.currFocusView)
    uvm.renderScreen()

def search(uvm, uFilter):
    preCommand(uvm)
    uvm.currFocusView.filterView(uFilter)

def thread(uvm, boardString, threadNumber):
    preCommand(uvm)
    uvm.allViews.contents[uvm.allViews.focus_position] = (View(uvm, ThreadFrame(boardString, threadNumber, uvm)), uvm.allViews.options())
    postCommand(uvm)

def board(uvm, boardString):
    preCommand(uvm)
    DEBUG('executing board command')
    uvm.allViews.contents[uvm.allViews.focus_position] = (View(uvm, BoardFrame(boardString, uvm)), uvm.allViews.options())
    postCommand(uvm)

def site(uvm):
    preCommand(uvm)
    if uvm.site is SITE.FCHAN:
        uvm.allViews.contents[uvm.allViews.focus_position] = (View(uvm, IndexFrame(uvm)), uvm.allViews.options())
    postCommand(uvm)

def history(uvm):
    preCommand(uvm)
    # uvm.currFocusView.setFrame(HistoryFrame(uvm))

def split(uvm, splitType, splitView):
    DEBUG(type(uvm.allViews))
    DEBUG(uvm.currFocusView.base_widget)
    # DEBUG(uvm.allViews.focus)
    if splitType == 0:
        if type(uvm.allViews) is urwid.Pile:
            DEBUG('Pile supertype')
            uvm.allViews.contents.append((View(uvm), uvm.allViews.options()))
        else:
            DEBUG(uvm.allViews.contents)
            uvm.allViews.contents[uvm.allViews.focus_position] = (urwid.Pile([uvm.currFocusView, View(uvm)]), uvm.allViews.options())
    elif splitType == 1:
        if type(uvm.allViews) is urwid.Columns:
            DEBUG('Columns supertype')
            uvm.allViews.contents.append((View(uvm), uvm.allViews.options()))
        else:
            uvm.allViews.contents[uvm.allViews.focus_position] = (urwid.Columns([uvm.currFocusView, View(uvm)]), uvm.allViews.options())

    uvm.buildAddHeaderView(uvm.currFocusView)
    uvm.buildAddFooterView(uvm.currFocusView)
    uvm.renderScreen()