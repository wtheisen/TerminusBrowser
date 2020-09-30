# Initial testing
import sys, urwid, time, os
import requests, json, collections, re

import urwid.raw_display
import urwid.web_display

from enum import Enum

from config import Config
from views.view_class import View
from frames.default_frame import DefaultFrame

from split_tracker import Column, Row, buildUrwidFromSplits

from custom_urwid_classes import CommandBar, HistoryButton
from command_handler_class import CommandHandler
from customer_types import LEVEL, MODE, SITE, STICKIES

# from commandChanVim import urwidView
from terminus_browser import urwidView

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
