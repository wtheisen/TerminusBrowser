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
    view = urwidView(True)
    return view

def test_init(view):
    assert view.mode   == MODE.NORMAL
    assert view.stickies == STICKIES.HIDE
    assert view.boardList == view.cfg.get('FCHAN')['boards']
    assert view.subredditList == view.cfg.get('REDDIT')['boards']

def test_handleKeyCommand(view):
    view.handleKey(':')
    assert view.mode == MODE.COMMAND

