# test_fchan.py

import sys

from terminus_browser import urwidView
from customer_types import SITE

from frames.fchan.index_frame import IndexFrame
from frames.fchan.board_frame import BoardFrame
from frames.fchan.thread_frame import ThreadFrame

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
