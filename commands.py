from boardClass import Board
from threadClass import Thread
from customeTypes import LEVEL, MODE

def preCommand(uvm):
    uvm.commandBar.set_caption('')
    uvm.mode = MODE.NORMAL
    uvm.frame.focus_position = 'body'

def search(uvm):
    preCommand(uvm)
    if uvm.level is LEVEL.INDEX:
        uvm.buildStartView()
    elif uvm.level is LEVEL.BOARD:
        uvm.board = Board(uvm)
    elif uvm.level is LEVEL.THREAD:
        uvm.thread = Thread(uvm)

    uvm.userFilter = None
    uvm.buildAddHeaderView()
    uvm.buildAddFooterView()
    uvm.displayFrame()

def thread(uvm):
    preCommand(uvm)
    if uvm.level is LEVEL.BOARD:
        uvm.thread = Thread(uvm)
        uvm.buildAddHeaderView()
        uvm.buildAddFooterView()
        uvm.displayFrame()

def site(uvm):
    preCommand(uvm)

    uvm.boards = uvm.cfg.config[uvm.site.name]['boards']

    uvm.level = LEVEL.INDEX
    uvm.buildStartView()

    uvm.userFilter = None
    uvm.buildAddHeaderView()
    uvm.buildAddFooterView()
    uvm.displayFrame()

def history(uvm):
    preCommand(uvm)
    uvm.thread = Thread(uvm)
    uvm.buildAddHeaderView()
    uvm.buildAddFooterView()
    uvm.displayFrame()

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
