import sys, urwid, time, os
import requests, json, collections, re

import urwid.raw_display
import urwid.web_display

from enum import Enum

from config import Config
from viewClass import View
from Frames.defaultFrame import DefaultFrame
from debug import INITDEBUG, DEBUG

from customUrwidClasses import CommandBar, HistoryButton
from commandHandlerClass import CommandHandler
from customeTypes import LEVEL, MODE, SITE

################################################################################

class urwidView():
    def __init__(self):
        self.mode   = MODE.NORMAL
        self.cfg    = Config('./default_config.json')
        self.site   = SITE[self.cfg.config['SITE']]
        self.boardList = self.cfg.config[self.site.name]['boards']
        self.commandHandler = CommandHandler(self)

        self.commandBar = CommandBar(lambda: self._update_focus(True), self)

        urwid.connect_signal(self.commandBar, 'command_entered', self.commandHandler.evalCommand)
        urwid.connect_signal(self.commandBar, 'exit_command', self.exitCommand)

        self.history = collections.deque([], 50)

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

        self.buildSetStartView()
        self.body = None
        self.allViews = urwid.Columns([self.currFocusView])

        self.buildAddHeaderView(self.currFocusView)
        self.buildAddFooterView(self.currFocusView)

        self.renderScreen()

    def exitCommand(self):
        self.mode = MODE.NORMAL
        self.buildAddFooterView(self.currFocusView)
        self.commandBar.set_caption('')
        self.body.focus_position = 'body'
        self.renderScreen()

    def _update_focus(self, focus):
        self._focus=focus

    def buildAddHeaderView(self, focusView):
        try:
            headerWidget = urwid.AttrWrap(urwid.Text(focusView.frame.headerString), 'header')
        except:
            headerWidget = urwid.AttrWrap(urwid.Text(''), 'header')

        # self.allViews = self.currFocusView.view
        self.body = urwid.Frame(urwid.AttrWrap(self.allViews, 'body'))
        self.body.header = headerWidget

    def buildAddFooterView(self, focusView):
        try:
            footerStringLeft = urwid.AttrWrap(urwid.Text('Mode: ' + str(self.mode) + ', Filter: ' + str(self.currFocusView.uFilter)), 'header')
            footerStringRight = urwid.AttrWrap(urwid.Text(focusView.frame.footerStringRight, 'right'), 'header')
        except:
            footerStringLeft = urwid.Text('')
            footerStringRight = urwid.Text('')


        footerWidget = urwid.Pile([urwid.Columns([footerStringLeft, footerStringRight]), self.commandBar])
        self.body.footer = footerWidget

    def buildSetStartView(self):
        self.currFocusView = View(self, DefaultFrame(True))
        # self.currFocusView = View(self)

    def renderScreen(self):
        urwid.MainLoop(self.body,
                       self.palette,
                       self.screen,
                       unhandled_input=self.handleKey,
                       pop_ups=True).run()

    def handleKey(self, key):
        if key == ':':
            self.mode = MODE.COMMAND
            self.commandBar.set_caption(':')
            self.body.focus_position = 'footer'
            self.renderScreen()

        if self.mode is MODE.NORMAL:
            DEBUG(key)
            if key == 'h':
                self.body.keypress((100,100), 'left')
            if key == 'j':
                self.body.keypress((150,100), 'down')
            if key == 'k':
                self.body.keypress((150,100), 'up')
            if key == 'l':
                self.body.keypress((100,100), 'right')
            if key == 'r':
                pass

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
