from commandChanVim import urwidView
from Commands.SystemCommands import systemCommands
from Frames.reddit.indexFrame import RedditIndexFrame
from Frames.fchan.indexFrame import IndexFrame
from Frames.defaultFrame import DefaultFrame
from customeTypes import SITE

import pytest

@pytest.fixture
def view():
    view = urwidView(True)
    return view

test_boards = [
      ('add 4chan /r9k/', ['/r9k/']),
          ('add 4chan /r9k/ /s4s/', ['/r9k/', '/s4s/'])


  ]
@pytest.mark.parametrize("test_input, expected", test_boards)
def test_addChan(test_input, expected, view):
    systemCommands(test_input, view)
    result = all(ex in view.boardList for ex in expected)
    assert result

test_subs = [
    ('add reddit linuxgaming', ['linuxgaming']),
    ('add reddit linuxgaming sysadmin', ['linuxgaming', 'sysadmin'])
]
@pytest.mark.parametrize("test_input, expected", test_subs)
def test_addReddit(test_input, expected, view):
    systemCommands(test_input, view)
    result = all(ex in view.subredditList for ex in expected)
    assert result


test_views = [
    ('view reddit', [SITE.REDDIT, RedditIndexFrame]),
        ('view 4chan', [SITE.FCHAN, IndexFrame]),
            ('view too long', [None, DefaultFrame])

]
@pytest.mark.parametrize("test_input, expected", test_views)
def test_view(test_input, expected, view):
    systemCommands(test_input, view)
    assert view.currFocusView.site == expected[0]
    assert type(view.currFocusView.frame) == expected[1]
