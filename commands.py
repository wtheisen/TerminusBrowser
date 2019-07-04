from boardClass import Board
from threadClass import Thread
from customeTypes import LEVEL, MODE

def preCommand(uvm):
    uvm.commandBar.set_caption('')
    uvm.mode = MODE.NORMAL
    uvm.frame.focus_position = 'body'

def search(uvm):
    if uvm.level == LEVEL.BOARD:
        preCommand(uvm)
        uvm.board = Board(uvm)
        uvm.buildAddFooterView()
        uvm.displayFrame()

def thread(uvm):
    if uvm.level == LEVEL.BOARD:
        preCommand(uvm)
        uvm.thread = Thread(uvm)
        uvm.buildAddFooterView()
        uvm.displayFrame()
