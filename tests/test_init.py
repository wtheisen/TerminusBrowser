# Initial testing
import sys, urwid, time, os
import requests, json, collections, re

import urwid.raw_display
import urwid.web_display

from enum import Enum

from config import Config
from boardClass import Board
from threadClass import Thread

from customUrwidClasses import CommandBar, HistoryButton
from commandHandlerClass import CommandHandler
from customeTypes import LEVEL, MODE, SITE, STICKIES

from commandChanVim import urwidView

import threading
import pytest

@pytest.fixture
def view():
    view = urwidView()
    return view

def test_init(view):
    assert view.level == LEVEL.INDEX
    assert view.mode   == MODE.NORMAL
    assert view.stickies == STICKIES.HIDE
    assert view.site   == SITE[view.cfg.get('SITE')]
    assert view.boards == view.cfg.get(view.site.name)['boards']

# test commandBar, commandHandler, and HistoryButton