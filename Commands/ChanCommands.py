from debug import DEBUG
from viewClass import View

from Frames.boardFrame import BoardFrame
from Frames.threadFrame import ThreadFrame

def chanCommands(cmd, uvm):
    cmd = cmd.split()

    if cmd[0] in ('b', 'board'):
        DEBUG('executing board command')
        board(uvm, cmd[1])
    if cmd[0] in ('t', 'thread'):
        DEBUG('executing thread command')
        thread(uvm, cmd[1])

def board(uvm, boardString):
    DEBUG('Executing board command')
    setattr(uvm.currFocusView, 'frame', BoardFrame(boardString, uvm))
    # uvm.allViews = View(uvm, BoardFrame(boardString, uvm))

def thread(uvm, boardString, threadNumber):
    DEBUG('Executing thread command')
    uvm.allViews = View(uvm, ThreadFrame(boardString, threadNumber, uvm))