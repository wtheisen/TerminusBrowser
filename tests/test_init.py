# Initial testing
import sys, urwid, time, os
import requests, json, collections, re

import urwid.raw_display
import urwid.web_display

from enum import Enum

from config import Config
from Views.viewClass import View
from Frames.defaultFrame import DefaultFrame
from debug import INITDEBUG, DEBUG

from splitTracker import Column, Row, buildUrwidFromSplits

from customUrwidClasses import CommandBar, HistoryButton
from commandHandlerClass import CommandHandler
from customeTypes import LEVEL, MODE, SITE, STICKIES

from commandChanVim import urwidView

import pytest

@pytest.fixture
def view():
    view = urwidView()
    return view

def test_init(view):
    assert view.mode   == MODE.NORMAL
    assert view.stickies == STICKIES.HIDE
    assert view.site   == SITE[view.cfg.get('SITE')]
    assert view.boardList == view.cfg.get(view.site.name)['boards']

def test_buildSetStartView(view):
    pass

def test_buildAddHeaderView():
    pass

def test_buildAddFooterView():
    pass

def test_exitCommand():
    pass

def test_handleKeyCommand(view):
    view.handleKey(':')
    assert view.mode == MODE.COMMAND
    
