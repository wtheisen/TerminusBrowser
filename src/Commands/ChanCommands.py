from Views.viewClass import View
from customeTypes import SITE

from Frames.defaultFrame import FrameFactory

import Frames.fchan.boardFrame as fchanBoard
import Frames.fchan.threadFrame as fchanThread

import Frames.lchan.boardFrame as lchanBoard
import Frames.lchan.threadFrame as lchanThread

import logging
log = logging.getLogger(__name__)

ChanCommandList = [
    'b', 'board',
    't', 'thread'
]

def chanCommands(cmd, uvm):
    log.debug(cmd)
    cmd, *args = cmd.split()

    if cmd in ('b', 'board'):
        log.debug('executing board command')
        # uvm.currFocusView.updateHistory(f'setattr(uvm.currFocusView, "frame", BoardFrame("{args[0]}", uvm))')
        board(uvm, args[0])
    if cmd in ('t', 'thread'):
        log.debug('executing thread command')
        # uvm.currFocusView.updateHistory(f'setattr(uvm.currFocusView, "frame", ThreadFrame("{args[0]}", "{cmd[2]}", uvm))')
        thread(uvm, args[0], args[1])

    log.debug(uvm.history)

def board(uvm, boardString):
    log.debug('Executing board command')
    try:
        if uvm.currFocusView.site == SITE.FCHAN:
            setattr(uvm.currFocusView, 'frame', fchanBoard.BoardFrame(boardString, uvm))
            uvm.currFocusView.updateHistory(FrameFactory(fchanBoard.BoardFrame), [boardString, uvm])
        elif uvm.currFocusView.site is SITE.LCHAN:
            setattr(uvm.currFocusView, 'frame', lchanBoard.BoardFrame(boardString, uvm))
            uvm.currFocusView.updateHistory(FrameFactory(lchanBoard.BoardFrame), [boardString, uvm])
    except:
        uvm.currFocusView.frame.headerString = f'Error connecting to board {boardString}, does it exist?'
        log.debug(f'Error connecting to board {boardString}, does it exist?')

def thread(uvm, boardString, threadNumber):
    log.debug('Executing thread command')
    if uvm.currFocusView.site is SITE.FCHAN:
        uvm.currFocusView.updateHistory(FrameFactory(fchanThread.ThreadFrame), [boardString, threadNumber, uvm])
        setattr(uvm.currFocusView, 'frame', fchanThread.ThreadFrame(boardString, threadNumber, uvm))
    elif uvm.currFocusView.site is SITE.LCHAN:
        uvm.currFocusView.updateHistory(FrameFactory(lchanThread.ThreadFrame), [boardString, threadNumber, uvm])
        setattr(uvm.currFocusView, 'frame', lchanThread.ThreadFrame(boardString, threadNumber, uvm))
