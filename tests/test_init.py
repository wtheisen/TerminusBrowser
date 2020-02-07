# Initial testing
import sys, urwid, time, os
import requests, json, collections, re

import urwid.raw_display
import urwid.web_display

from enum import Enum

from config import Config
from Views.viewClass import View
from Frames.defaultFrame import DefaultFrame

from splitTracker import Column, Row, buildUrwidFromSplits

from customUrwidClasses import CommandBar, HistoryButton
from commandHandlerClass import CommandHandler
from customeTypes import LEVEL, MODE, SITE, STICKIES

# from commandChanVim import urwidView
from TerminusBrowser import urwidView

import pytest

import logging
log = logging.getLogger(__name__)

@pytest.fixture
def view():
    view = urwidView(True)
    return view

def test_init(view):
    assert view.mode   == MODE.NORMAL
    assert view.stickies == STICKIES.HIDE

def test_handleKeyCommand(view):
    view.handleKey(':')
    assert view.mode == MODE.COMMAND

