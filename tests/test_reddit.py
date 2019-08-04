# test_fchan.py

import sys

from commandChanVim import urwidView

from Frames.reddit.indexFrame import RedditIndexFrame
from Frames.reddit.subredditFrame import SubredditFrame

import pytest

test_list = [
    ('view reddit', RedditIndexFrame),
    ('sub /r/all', SubredditFrame),
]

@pytest.mark.parametrize('test_input, expected', test_list)
def test_fchan(test_input, expected):
    uvm = urwidView()
    uvm.commandHandler.routeCommand(test_input)
    assert type(uvm.currFocusView.frame) == expected