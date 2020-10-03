from views.view_class import View
from customer_types import SITE

from frames.default_frame import FrameFactory

import frames.fchan.board_frame as fchanBoard
import frames.fchan.thread_frame as fchanThread

import frames.lchan.board_frame as lchanBoard
import frames.lchan.thread_frame as lchanThread

from helper_functions import downloadThreadImages, PostReply

import logging
log = logging.getLogger(__name__)

post = None

ChanCommandList = [
    'b', 'board',
    't', 'thread',
    'd', 'download',
    'c', 'captcha'
]

def chanCommands(cmd, uvm):
    global post
    log.debug(cmd)
    cmd, *args = cmd.split()

    if cmd in ('b', 'board') and len(args) == 1:
        log.debug('executing board command')
        # uvm.currFocusView.updateHistory(f'setattr(uvm.currFocusView, "frame", BoardFrame("{args[0]}", uvm))')
        board(uvm, args[0])
    if cmd in ('t', 'thread') and len(args) == 2:
        log.debug('executing thread command')
        # uvm.currFocusView.updateHistory(f'setattr(uvm.currFocusView, "frame", ThreadFrame("{args[0]}", "{cmd[2]}", uvm))')
        thread(uvm, args[0], args[1])
    if cmd in ('d', 'download'):
        log.debug('executing download command')
        t = uvm.currFocusView.frame
        downloadThreadImages(t.comments,
                             uvm,
                             f'./Pictures/{t.boardString.strip("/")}/{str(t.threadNumber)}')
    if cmd in ('p', 'post') and len(args) >= 2:
        log.debug('executing post command')
        t = uvm.currFocusView.frame
        post = uploadPost(uvm, t.boardString.strip('/'), str(t.threadNumber), args[0], ' '.join(args[1:]))
        post.startChanPost()

    if cmd in ('c', 'captcha'):
        log.debug('Captcha answered')
        post.endChanPost(args)

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

class uploadPost():
    def __init__(self, uvm, boardString, threadNumber, fullFilePath, comment):
        self.uvm = uvm
        self.boardString = boardString
        self.threadNumber = threadNumber
        self.fullFilePath = fullFilePath
        self.comment = comment

        self.p = PostReply(self.boardString, self.threadNumber)

    def startChanPost(self):
        self.p.get_captcha_challenge()
        self.p.display_captcha()

    def endChanPost(self, answers):
        self.p.set_captcha2_solution(''.join(answers))
        self.p.post(comment=self.comment, file_attach=self.fullFilePath)
