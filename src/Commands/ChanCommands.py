from debug import DEBUG
from Views.viewClass import View

from Frames.fchan.boardFrame import BoardFrame
from Frames.fchan.threadFrame import ThreadFrame

def chanCommands(cmd, uvm):
    cmd = cmd.split()

    if cmd[0] in ('b', 'board'):
        DEBUG('executing board command')
        # uvm.currFocusView.updateHistory(f'setattr(uvm.currFocusView, "frame", BoardFrame("{cmd[1]}", uvm))')
        board(uvm, cmd[1])
    if cmd[0] in ('t', 'thread'):
        DEBUG('executing thread command')
        # uvm.currFocusView.updateHistory(f'setattr(uvm.currFocusView, "frame", ThreadFrame("{cmd[1]}", "{cmd[2]}", uvm))')
        thread(uvm, cmd[1], cmd[2])

    DEBUG(uvm.history)

def board(uvm, boardString):
    DEBUG('Executing board command')
    try:
        setattr(uvm.currFocusView, 'frame', BoardFrame(boardString, uvm))
        uvm.currFocusView.updateHistory(BoardFrame.BoardFrameFactory, [boardString, uvm])
    except:
        uvm.currFocusView.frame.headerString = f'Error connecting to board {boardString}, does it exist?'
        DEBUG(f'Error connecting to board {boardString}, does it exist?')
    # uvm.allViews = View(uvm, BoardFrame(boardString, uvm))

def thread(uvm, boardString, threadNumber):
    DEBUG('Executing thread command')
    uvm.currFocusView.updateHistory(ThreadFrame.ThreadFrameFactory, [boardString, threadNumber, uvm])
    setattr(uvm.currFocusView, 'frame', ThreadFrame(boardString, threadNumber, uvm))
