# test_fchan.py

import sys

from TerminusBrowser import urwidView
from customeTypes import SITE

from Frames.fchan.indexFrame import IndexFrame
from Frames.fchan.boardFrame import BoardFrame
from Frames.fchan.threadFrame import ThreadFrame

import pytest

test_list = [
    ('view 4chan', None, IndexFrame),
    ('board /g/', SITE.LCHAN, BoardFrame),
    ('thread /g/ 76759434', SITE.LCHAN, ThreadFrame) #This is the /g/ sticky so this number is always valid
]

@pytest.mark.parametrize('test_input,site,expected', test_list)
def test_fchan(test_input, site, expected):
    uvm = urwidView(True)
    uvm.currFocusView.site = SITE.FCHAN

    uvm.commandHandler.routeCommand(test_input)

    assert type(uvm.currFocusView.frame) == expected
