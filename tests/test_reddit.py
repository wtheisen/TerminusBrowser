# test_fchan.py

import sys

# from commandChanVim import urwidView
from terminus_browser import urwidView

from frames.reddit.index_frame import RedditIndexFrame
from frames.reddit.subreddit_frame import SubredditFrame

import pytest

test_list = [
    ('view reddit', RedditIndexFrame),
    ('sub /r/all', SubredditFrame),
]

@pytest.mark.parametrize('test_input, expected', test_list)
def test_fchan(test_input, expected):
    uvm = urwidView(True)
    uvm.commandHandler.routeCommand(test_input)
    assert type(uvm.currFocusView.frame) == expected
