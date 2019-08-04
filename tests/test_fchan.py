# test_fchan.py

import sys

from commandChanVim import urwidView
from commandHandlerClass import CommandHandler

from Frames.fchan.indexFrame import IndexFrame
from Frames.fchan.boardFrame import BoardFrame
from Frames.fchan.threadFrame import ThreadFrame

import pytest

test_list = [
    ('view 4chan', IndexFrame),
    ('board /g/', BoardFrame),
    ('thread /g/ 51971506', ThreadFrame) #This is the /g/ sticky so this number is always valid
]

@pytest.mark.parametrize('test_input, expected', test_list)
def test_fchan(test_input, expected):
    uvm = urwidView()
    uvm.commandHandler.routeCommand(test_input)
    assert type(uvm.currFocusView.frame) == expected
