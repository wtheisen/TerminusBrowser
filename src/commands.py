import urwid

from view_class import View

from frames.index_frame import IndexFrame
from frames.board_frame import BoardFrame
from frames.thread_frame import ThreadFrame

from customer_types import LEVEL, MODE, SITE

import logging
log = logging.getLogger(__name__)

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
    uvm.allViews = View(uvm, ThreadFrame(boardString, threadNumber, uvm))
    postCommand(uvm)

def board(uvm, boardString):
    preCommand(uvm)
    log.debug('executing board command')
    # uvm.allViews.contents[uvm.allViews.focus_position] = (View(uvm, BoardFrame(boardString, uvm)), uvm.allViews.options())
    uvm.allViews = View(uvm, BoardFrame(boardString, uvm))
    postCommand(uvm)

def site(uvm):
    preCommand(uvm)
    if uvm.site is SITE.FCHAN:
        log.debug(uvm.allViews.focus)
        uvm.allViews = View(uvm, IndexFrame(uvm))
        # uvm.currFocusView.setFrame(IndexFrame(uvm))
        # setattr(uvm.currFocusView, 'frame', IndexFrame(uvm))
        # uvm.currFocusView = View(uvm, IndexFrame(uvm))
        # uvm.allViews.set_focus = (View(uvm, IndexFrame(uvm)), uvm.allViews.options())
    postCommand(uvm)

def history(uvm):
    preCommand(uvm)
    # uvm.currFocusView.setFrame(HistoryFrame(uvm))

def split(uvm, splitType, splitView):
    log.debug(type(uvm.allViews))
    log.debug(uvm.allViews.focus)
    if splitType == 0:
        if type(uvm.allViews) is urwid.Pile:
            log.debug('Pile supertype')
            uvm.allViews.contents.append((View(uvm), uvm.allViews.options()))
        else:
            log.debug(uvm.allViews.contents)
            uvm.allViews.focus = urwid.Pile([uvm.currFocusView, View(uvm)])
    elif splitType == 1:
        if type(uvm.allViews) is urwid.Columns:
            log.debug('Columns supertype')
            uvm.allViews.contents.append((View(uvm), uvm.allViews.options()))
        else:
            uvm.allViews.focus = urwid.Columns([uvm.currFocusView, View(uvm)])

    postCommand(uvm)

# For toggling stickies, auto refresh. Could use this func in other places if wish to rebase a lil
def refresh(uvm):
    uvm.mode = MODE.NORMAL
    if uvm.level is LEVEL.BOARD:
        uvm.displayBoard(uvm, uvm.boardString)
    elif uvm.level is LEVEL.THREAD:
        uvm.displayThread(uvm, uvm.threadID)
    uvm.buildAddHeaderView()
    uvm.buildAddFooterView()
    uvm.displayFrame()
