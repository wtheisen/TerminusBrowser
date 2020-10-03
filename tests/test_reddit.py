# test_fchan.py

import sys

# from commandChanVim import urwidView
from TerminusBrowser import urwidView

from Frames.reddit.indexFrame import RedditIndexFrame
from Frames.reddit.subredditFrame import SubredditFrame

from src.customeTypes import SITE

import pytest


test_list = [
    ('view reddit', None, RedditIndexFrame),
    ('sub /r/all', SITE.REDDIT, SubredditFrame),
]


@pytest.mark.parametrize('test_input,site,expected', test_list)
def test_reddit(test_input, site, expected):
    uvm = urwidView(True)
    uvm.currFocusView.site = site

    uvm.commandHandler.routeCommand(test_input)

    assert type(uvm.currFocusView.frame) == expected
