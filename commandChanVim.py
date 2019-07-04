import sys, urwid, time
import requests, json, collections, re

import urwid.raw_display
import urwid.web_display

from bs4 import BeautifulSoup
from enum import Enum

from boardClass import Board
from threadClass import Thread
from debug import INITDEBUG, DEBUG

from customUrwidClasses import CommandBar
from commandHandlerClass import CommandHandler
from customeTypes import LEVEL, MODE

################################################################################

boards = ['/g/', '/v/', '/tv/', '/sp/', '/fa/', '/pol/', '/vg/',
          '/a/', '/b/', '/c/', '/d/', '/e/',
          '/f/', '/gif/', '/h/', '/hr/', '/k/',
          '/m/', '/o/', '/p/', '/r/', '/s/',
          '/t/', '/u/', '/vr/',
          '/w/', '/wg/', '/i/', '/ic/', '/r9k/',
          '/s4s/', '/vip/', '/cm/', '/hm/', '/lgbt/',
          '/y/', '/3/', '/aco/', '/adv/', '/an/',
          '/asp/', '/bant/', '/biz/', '/cgl/', '/ck/',
          '/co/', '/diy/', '/fit/', '/gd/', '/hc/',
          '/his/', '/int/', '/jp/', '/lit/', '/mlp/',
          '/mu/', '/n/', '/news/', '/out/', '/po/',
          '/qst/', '/sci/', '/soc/', '/tg/', 'toy',
          '/trv/', '/vp/', '/wsg/', '/wsr/', '/x/']

################################################################################

class urwidView():
    def __init__(self):
        self.level = LEVEL.INDEX
        self.mode = MODE.NORMAL
        self.commandHandler = CommandHandler(self)

        self.commandBar = CommandBar(lambda: self._update_focus(True), self)

        urwid.connect_signal(self.commandBar, 'command_entered', self.commandHandler.evalCommand)
        urwid.connect_signal(self.commandBar, 'exit_command', self.exitCommand)

        self.boardString = 'Index'
        self.threadNum = 0
        self.userFilter = None

        self.itemCount = len(boards)
        self.parseTime = 0

        self.palette = [
        ('body', 'light gray', 'black', 'standout'),
        ('quote', 'light cyan', 'black'),
        ('greenText', 'dark green', 'black'),
        ('header', 'white', 'dark red', 'bold'),
        ('quotePreview', 'light gray', 'black')
        ]

        # use appropriate Screen class
        if urwid.web_display.is_web_request():
            self.screen = urwid.web_display.Screen()
        else:
            self.screen = urwid.raw_display.Screen()

        self.frame = None
        self.indexView = None

        self.buildHeaderView()
        self.buildStartView()
        self.buildAddFooterView()

        self.displayFrame()

    def exitCommand(self):
        self.mode = MODE.NORMAL
        self.buildAddFooterView()
        self.commandBar.set_caption('')
        self.frame.focus_position = 'body'
        self.displayFrame()

    def _update_focus(self, focus):
        self._focus=focus

    def buildHeaderView(self):
        self.header = urwid.AttrWrap(urwid.Text('CommandChan'), 'header')

    def buildAddFooterView(self):
        infoString = urwid.AttrWrap(urwid.Text('Mode: ' + str(self.mode) + ', Board: ' + self.boardString), 'header')
        timeString = urwid.AttrWrap(urwid.Text('Parsed ' + str(self.itemCount) + ' items in ' + str(self.parseTime)[0:6] + 's', 'right'), 'header')
        footerWidget = urwid.Pile([urwid.Columns([infoString, timeString]), self.commandBar])
        self.frame.footer = footerWidget

    def buildStartView(self):
        startTime = time.time()

        boardButtons = []
        for board in boards:
            boardButtons.append(urwid.LineBox(urwid.AttrWrap(urwid.Button(board, self.displayBoard), 'center')))

        buttonGrid = urwid.GridFlow(boardButtons, 12, 2, 2, 'center')
        listbox_content = [buttonGrid]

        test = urwid.ListBox(urwid.SimpleListWalker(listbox_content))

        self.frame = urwid.Frame(urwid.AttrWrap(test, 'body'), header=self.header)
        self.indexView = self.frame

        endTime = time.time()
        self.parseTime = (endTime - startTime)

    def displayFrame(self):
        urwid.MainLoop(self.frame,
                       self.palette,
                       self.screen,
                       unhandled_input=self.handleKey,
                       pop_ups=True).run()

    def displayStartView(self):
        self.frame = self.indexView
        self.displayFrame()

    def displayBoard(self, button, board=None, userFilter=None):
        self.level = LEVEL.BOARD

        if board:
            self.board = Board(self)
        else:
            self.boardString = button.get_label()
            self.board = Board(self)

        self.buildAddFooterView()
        self.displayFrame()

    def displayThread(self, button, board=None, userFilter=None):
        self.level = LEVEL.THREAD
        self.threadNum = button.get_label()

        self.thread = Thread(self)

        self.buildAddFooterView()
        self.displayFrame()


    def handleKey(self, key):
        if key == ':':
            self.mode = MODE.COMMAND
            self.buildAddFooterView()
            self.commandBar.set_caption(':')
            self.frame.focus_position = 'footer'
            self.displayFrame()

        if self.mode is MODE.NORMAL:
            DEBUG(key)
            if key == 'h':
                self.frame.keypress((1000,1000), 'left')
            if key == 'j':
                self.frame.keypress((1000,1000), 'down')
            if key == 'k':
                self.frame.keypress((1000,1000), 'up')
            if key == 'l':
                self.frame.keypress((1000,1000), 'right')
            if key == 'r':
                if self.level is LEVEL.BOARD:
                    self.displayBoard(self, self.boardString)
                elif self.level is LEVEL.THREAD:
                    self.displayThread(self, self.threadNum)
            elif key == 'q':
                if self.level is LEVEL.INDEX:
                    sys.exit()
                elif self.level is LEVEL.BOARD:
                    self.level = LEVEL.INDEX
                    self.board = ''
                    self.userFilter = ''
                    self.displayStartView()
                elif self.level is LEVEL.THREAD:
                    self.level = LEVEL.BOARD
                    self.userFilter = ''
                    self.displayBoard(None, self.board)
                    self.displayFrame()

################################################################################

def main():
    u = urwidView()

def setup():
    urwid.web_display.set_preferences("Urwid Tour")
    # try to handle short web requests quickly
    if urwid.web_display.handle_short_request():
        return

    main()

if '__main__'==__name__ or urwid.web_display.is_web_request():
    INITDEBUG()
    setup()
