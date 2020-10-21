# from commandChanVim import urwidView
from terminus_browser import urwidView
from commands.system_commands import systemCommands
from frames.reddit.index_frame import RedditIndexFrame
from frames.fchan.index_frame import IndexFrame as fchanIndexFrame
from frames.lchan.index_frame import IndexFrame as lchanIndexFrame
from frames.hackernews.index_frame import HackerNewsIndexFrame

from frames.default_frame import DefaultFrame
from frames.history_frame import HistoryFrame
import frames.lchan.index_frame as lIndex

from customer_types import SITE

import unittest
import pytest

@pytest.fixture
def view():
    view = urwidView(True)
    return view

@pytest.fixture()
def write_source_files(tmpdir):
    with tmpdir.as_cwd() as dir:
        source_hash = dir.join("hash.txt")
        source_hash.write("# I like bananies")

        print(source_hash.read())

        source_vr = dir.join("vr.txt")
        source_vr.write("view reddit")


test_boards = [
      ('add 4chan /r9k/', ['/r9k/']),
          ('add 4chan /r9k/ /s4s/', ['/r9k/', '/s4s/'])


  ]
@pytest.mark.parametrize("test_input, expected", test_boards)
def test_addChan(test_input, expected, view):
    systemCommands(test_input, view)
    result = all(ex in view.cfg.deep_get(SITE.FCHAN, 'boards') for ex in expected)
    assert result

test_set = [
    ('set test ahoy'),
    ('set REDDIT username test')
]
@pytest.mark.parametrize("test_input", test_set)
def test_setCommand(test_input, view):
    systemCommands(test_input, view)

    cmd = test_input.split()
    if len(cmd) == 3:
        assert view.cfg.get(cmd[1]) == cmd[2]
    else:
        assert view.cfg.deep_get(cmd[1], cmd[2]) == cmd[3]


test_subs = [
    ('add reddit linuxgaming', ['linuxgaming']),
    ('add reddit linuxgaming sysadmin', ['linuxgaming', 'sysadmin'])
]
@pytest.mark.parametrize("test_input, expected", test_subs)
def test_addReddit(test_input, expected, view):
    systemCommands(test_input, view)
    result = all(ex in view.cfg.deep_get(SITE.REDDIT, 'boards') for ex in expected)
    assert result


test_views = [
    ('view rEdDiT', [SITE.REDDIT, RedditIndexFrame]),
    ('view 4ChaN', [SITE.FCHAN, fchanIndexFrame]),
    ('view hisTORy', [None, HistoryFrame]),
    ('view H', [None, HistoryFrame]),
    ('view too long', [None, DefaultFrame])

]
@pytest.mark.parametrize("test_input, expected", test_views)
def test_view(test_input, expected, view):
    systemCommands(test_input, view)
    assert type(view.currFocusView.frame) == expected[1]

test_quit = [
    ('q'),
    ('qa'),
    ('quitall')]

@pytest.mark.parametrize("test_input", test_quit)
def test_quit(test_input, view):
    with pytest.raises(SystemExit) as wrapped_e:
        systemCommands(test_input, view)
    assert wrapped_e.type == SystemExit

test_src = [
    ('source hash.txt', [None, DefaultFrame]),
    ('source vr.txt', [SITE.REDDIT, RedditIndexFrame]),
    ('source imaginary-file', [None, DefaultFrame])
]

@pytest.mark.parametrize("source, expected", test_src)
def test_source(source, expected, view, write_source_files):
    systemCommands(source, view)
    assert type(view.currFocusView.frame) == expected[1]


test_history = [
        (['view reddit', 'view 4chan'], 'h', [SITE.REDDIT, RedditIndexFrame]),
        (['view 4chan', 'view reddit'], 'history', [SITE.FCHAN, fchanIndexFrame]),
        (['view reddit', 'view 4chan'], 'h 1', [SITE.REDDIT, RedditIndexFrame]),
        (['view reddit', 'view 4chan'], 'h z', [SITE.FCHAN, fchanIndexFrame])
]

@pytest.mark.parametrize("cmd, history, expected", test_history)
def test_hist(cmd, history, expected, view):
    systemCommands(cmd[0], view)
    systemCommands(cmd[1], view)
    systemCommands(history, view)
    assert type(view.currFocusView.frame) == expected[1]

test_srch = [
    (['view reddit', 'view 4chan'], 's 4chan', [SITE.FCHAN, fchanIndexFrame]),
        (['view reddit', 'view 4chan'], 's reddit', [SITE.FCHAN, fchanIndexFrame]),
        (['view reddit', 'view 4chan'], 's hn', [SITE.FCHAN, fchanIndexFrame])]

@pytest.mark.parametrize("cmd, search, expected", test_srch)
def test_search(cmd, search, expected, view):
    systemCommands(cmd[0], view)
    systemCommands(cmd[1], view)
    systemCommands(search, view)
    assert type(view.currFocusView.frame) == expected[1]
