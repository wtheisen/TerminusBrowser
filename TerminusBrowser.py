#!/usr/bin/env python3
import sys, urwid, time, os
import requests, json, collections, re

import urwid.raw_display
import urwid.web_display

from enum import Enum

# add sys to path so you don't have to sys.
sys.path.append('src')

from config import Config
from Views.viewClass import View
from Frames.defaultFrame import DefaultFrame
from debug import setupLogger

from splitTracker import Column, Row, buildUrwidFromSplits

from customUrwidClasses import CommandBar, HistoryButton
from commandHandlerClass import CommandHandler
from customeTypes import LEVEL, MODE, SITE, STICKIES

import logging
log = logging.getLogger(__name__)

################################################################################

class urwidView():
    KEYMAP = {
        'h': 'left',
        'j': 'down',
        'k': 'up',
        'l': 'right'
    }

    def __init__(self, test=False):
        self.mode = MODE.NORMAL
        self.stickies = STICKIES.HIDE
        self.cfg = Config()
        self.test = test

        self.commandHandler = CommandHandler(self)

        self.commandBar = CommandBar(lambda: self._update_focus(True), self)

        urwid.connect_signal(self.commandBar, 'command_entered', self.commandHandler.routeCommand)
        urwid.connect_signal(self.commandBar, 'exit_command', self.exitCommand)

        self.idList = []
        self.history = []

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

        self.splitTuple = self.currFocusView

        self.buildAddHeaderView(self.currFocusView)
        self.buildAddFooterView(self.currFocusView)

    def getFreeID(self):
        ID = 1
        while ID in self.idList:
            ID += 1
        return ID

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

        builtUrwidSplits = buildUrwidFromSplits(self.splitTuple)
        log.debug(type(builtUrwidSplits))
        self.body = urwid.Frame(urwid.AttrWrap(builtUrwidSplits, 'body'))
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
        self.currFocusView = View(self, DefaultFrame(True, self.test))
        # self.currFocusView = View(self)

    def renderScreen(self):
        if __name__ == '__main__': # for testing purposes don't render outside file
            urwid.MainLoop(self.body,
                        self.palette,
                        self.screen,
                        unhandled_input=self.handleKey,
                        pop_ups=True).run()

    def handleKey(self, key):
        if not isinstance(key, tuple): # avoid mouse click event tuples
            if key == ':':
                self.mode = MODE.COMMAND
                self.commandBar.set_caption(':')
                self.body.focus_position = 'footer'
                self.renderScreen()


            if self.mode is MODE.NORMAL:
                if key.isalpha():
                    key = key.lower()

                if key not in urwidView.KEYMAP.keys():
                    return

                rows, cols = urwid.raw_display.Screen().get_cols_rows()
                self.body.keypress((rows, cols), urwidView.KEYMAP[key])

################################################################################

def main():
    u = urwidView()
    u.renderScreen()

def setup():
    urwid.web_display.set_preferences("Urwid Tour")
    # try to handle short web requests quickly
    if urwid.web_display.handle_short_request():
        return

    main()

def refresh_log():
    if os.path.exists("debug.log"):
        os.remove("debug.log")

if __name__ == '__main__' or urwid.web_display.is_web_request():
    refresh_log()
    setupLogger()
    setup()
