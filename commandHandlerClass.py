import urwid

from boardClass import Board
from debug import DEBUG
from customeTypes import LEVEL, MODE

commandList = [
    'search',
    'thread',
    'board',
    'post',
    'reply',
    'threadStyle',
    'boardStyle'
]

class CommandHandler:
    def __init__(self, urwidViewManager):
        self.defLeadChar = ':'
        self.uvm = urwidViewManager

    def evalCommand(self, cmd):
        DEBUG(cmd)

        if cmd.split()[0] in ('s' or 'search'):
            self.uvm.userFilter = cmd.split()[1]
            if self.uvm.level == LEVEL.BOARD:
                self.uvm.buildStartView()
                self.uvm.mode = MODE.NORMAL
                self.uvm.frame.focus_position = 'body'
                self.uvm.board = Board(self.uvm)
                self.uvm.buildAddFooterView()
                self.uvm.displayFrame()