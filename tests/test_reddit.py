# test_fchan.py

import sys

from commandChanVim import urwidView

from Frames.reddit.indexFrame import IndexFrame
from Frames.reddit.subredditFrame import SubredditFrame
from Frames.reddit.threadFrame import ThreadFrame

import pytest

test_list = [
    ('view reddit', IndexFrame),
    ('sub /r/all', SubredditFrame),
]

@pytest.mark.parametrize('test_input, expected', test_list)
def test_fchan(test_input, expected):
    uvm = urwidView()
    uvm.commandHandler.routeCommand(test_input)
    assert type(uvm.currFocusView.frame) == expected