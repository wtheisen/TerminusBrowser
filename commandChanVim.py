import sys, urwid, time, os
import requests, json, collections, re

import urwid.raw_display
import urwid.web_display

from enum import Enum

from config import Config
from boardClass import Board
from threadClass import Thread
from debug import INITDEBUG, DEBUG

from customUrwidClasses import CommandBar
from commandHandlerClass import CommandHandler
from customeTypes import LEVEL, MODE, SITE

################################################################################

class urwidView():
    def __init__(self):
        self.level  = LEVEL.INDEX
        self.mode   = MODE.NORMAL
        self.cfg    = Config('./default_config.json')
        self.site   = SITE[self.cfg.config['SITE']]
        self.boards = self.cfg.config[self.site.name]['boards']
        self.commandHandler = CommandHandler(self)

        self.commandBar = CommandBar(lambda: self._update_focus(True), self)

        urwid.connect_signal(self.commandBar, 'command_entered', self.commandHandler.evalCommand)
        urwid.connect_signal(self.commandBar, 'exit_command', self.exitCommand)

        self.boardString = 'Index'
        self.threadID = 0
        self.userFilter = None

        self.itemCount = len(self.boards)
        self.parseTime = 0

        self.history = collections.deque([], 10)

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

        self.buildStartView()
        self.buildAddHeaderView()
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

    def buildAddHeaderView(self):
        if self.site == SITE.FCHAN:
            header_text = 'CommandChan -- Board: {} Thread: {}'
        elif self.site == SITE.REDDIT:
            header_text = 'CommandChan -- Subreddit: {} Post: {}'
        else:
            header_text = 'Error: {} {}'

        header = urwid.AttrWrap(urwid.Text(header_text.format(self.boardString,str(self.threadID))), 'header')
        self.frame = urwid.Frame(urwid.AttrWrap(self.bodyView, 'body'), header=header)
        # self.frame = self.indexView

    def buildAddFooterView(self):
        infoString = urwid.AttrWrap(urwid.Text('Mode: ' + str(self.mode) +
                                               ', Filter: ' + str(self.userFilter)), 'header')
        timeString = urwid.AttrWrap(urwid.Text('Parsed ' + str(self.itemCount) + ' items in ' + str(self.parseTime)[0:6] + 's', 'right'), 'header')
        footerWidget = urwid.Pile([urwid.Columns([infoString, timeString]), self.commandBar])
        self.frame.footer = footerWidget

    def buildStartView(self):
        startTime = time.time()

        boardButtons = []
        for board in self.boards:
            if self.userFilter:
                if self.userFilter.lower() in board.lower():
                    boardButtons.append(urwid.LineBox(urwid.AttrWrap(urwid.Button(board, self.displayBoard), 'center')))
            else:
                boardButtons.append(urwid.LineBox(urwid.AttrWrap(urwid.Button(board, self.displayBoard), 'center')))

        buttonGrid = urwid.GridFlow(boardButtons, 12, 2, 2, 'center')
        listbox_content = [buttonGrid]

        self.indexView = urwid.ListBox(urwid.SimpleListWalker(listbox_content))
        self.bodyView = self.indexView

        endTime = time.time()
        self.parseTime = (endTime - startTime)
        self.itemCount = len(boardButtons)

    def displayFrame(self):
        urwid.MainLoop(self.frame,
                       self.palette,
                       self.screen,
                       unhandled_input=self.handleKey,
                       pop_ups=True).run()

    def displayStartView(self):
        self.bodyView = self.indexView
        self.buildAddHeaderView()
        self.buildAddFooterView()
        self.displayFrame()

    def displayBoard(self, button, board=None, userFilter=None):
        self.level = LEVEL.BOARD

        if board:
            self.board = Board(self)
        else:
            self.boardString = button.get_label()
            self.board = Board(self)

        self.buildAddHeaderView()
        self.buildAddFooterView()
        self.displayFrame()

    def displayThread(self, button, board=None, userFilter=None):
        self.level = LEVEL.THREAD
        self.threadID = button.get_label()

        self.history.appendleft(self.threadID)
        self.thread = Thread(self)

        self.buildAddHeaderView()
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
                self.frame.keypress((100,100), 'left')
            if key == 'j':
                self.frame.keypress((150,100), 'down')
            if key == 'k':
                self.frame.keypress((150,100), 'up')
            if key == 'l':
                self.frame.keypress((100,100), 'right')
            if key == 'r':
                if self.level is LEVEL.BOARD:
                    DEBUG('refreshing')
                    self.displayBoard(self, self.boardString)
                elif self.level is LEVEL.THREAD:
                    self.displayThread(self, self.threadID)
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
