import sys

from customeTypes import SITE
from Views.viewClass import View

from Frames.defaultFrame import FrameFactory
from Frames.historyFrame import HistoryFrame
from Frames.reddit.indexFrame import RedditIndexFrame
from Frames.hackernews.indexFrame import HackerNewsIndexFrame

import Frames.fchan.indexFrame as fIndex
import Frames.lchan.indexFrame as lIndex

from splitTracker import Row, Column

import logging
log = logging.getLogger(__name__)

SystemCommandList = [
    'add',
    's', 'search',
    'set',
    'source',
    'r', 'refresh',
    'split',
    'vsplit',
    'unsplit',
    'view',
    'h', 'history',
    'q',
    'qa', 'quitall'
]

def systemCommands(cmd, uvm):
    cmd = cmd.split()

    if cmd[0] in ('qa', 'quitall'):
        log.debug('Executing quit command')
        if uvm.cfg.update_file():
            log.debug('updated config')
        sys.exit()

    elif cmd[0] == ('add'):
        if len(cmd) >= 3:
            log.debug(f'Executing add command with args: {cmd[1:]}')
            if cmd[1] == '4chan':
                for board in cmd[2:]:
                    uvm.cfg.add_topic(SITE.FCHAN, board)
                    setattr(uvm.currFocusView, 'frame', fIndex.IndexFrame(uvm))
            elif cmd[1] == 'reddit':
                for subreddit in cmd[2:]:
                    uvm.cfg.add_topic(SITE.REDDIT, subreddit)
                    setattr(uvm.currFocusView, 'frame', RedditIndexFrame(uvm))

    elif cmd[0] == ('set'):
        # :set key value
        if len(cmd) == 3:
            uvm.cfg.set(cmd[1], cmd[2])
        # :set SITE key value
        elif len(cmd) == 4:
            uvm.cfg.deep_set(cmd[1], cmd[2], cmd[3])

    elif cmd[0] == ('source'):
        pass
        try:
            with open(cmd[1], 'r') as rcFile:
                for command in rcFile:
                    command = command.strip()
                    if command[0] != '#':
                        systemCommands(command, uvm)
        except:
            log.debug(f'ERROR: Unable to source {cmd[1]}')

    elif cmd[0] in ('h', 'history'):
        if len(cmd) is 2:
            h = uvm.history[int(cmd[1])]
            setattr(uvm.currFocusView, 'frame', h[1](h[2]))
        else:
            for h in uvm.history[1:]:
                if h[0] is uvm.currFocusView.id:
                    log.debug('Executing history command')
                    uvm.history.insert(0, h)
                    setattr(uvm.currFocusView, 'frame', h[1](h[2]))
                    break

    elif cmd[0] in ('s', 'search'):
        h = uvm.history[0]
        newArgs = h[2].copy()
        if len(cmd) is 2:
            newArgs.append(cmd[1])

        setattr(uvm.currFocusView, 'frame', h[1](newArgs))

    elif cmd[0] == ('view'):
        log.debug('executing site command')
        log.debug(cmd)
        if len(cmd) == 2:
            if cmd[1] in 'history':
                setattr(uvm.currFocusView, 'frame', HistoryFrame(uvm))
            elif cmd[1] == '4chan':
                log.debug('4chan requested')
                uvm.currFocusView.updateHistory(FrameFactory(fIndex.IndexFrame), [uvm])
                setattr(uvm.currFocusView, 'frame', fIndex.IndexFrame(uvm))
            elif cmd[1] == 'lainchan' or cmd[1] == 'lchan':
                log.debug('lainchan requested')
                uvm.currFocusView.updateHistory(FrameFactory(lIndex.IndexFrame), [uvm])
                setattr(uvm.currFocusView, 'frame', lIndex.IndexFrame(uvm))
            elif cmd[1] in ['reddit', 'Reddit']:
                log.debug('reddit requested')
                uvm.currFocusView.updateHistory(FrameFactory(RedditIndexFrame), [uvm])
                setattr(uvm.currFocusView, 'frame', RedditIndexFrame(uvm))
            elif cmd[1].lower() in ['hn', 'hackernews']:
                log.debug('HN requested')
                uvm.currFocusView.updateHistory(FrameFactory(HackerNewsIndexFrame), [uvm])
                setattr(uvm.currFocusView, 'frame', HackerNewsIndexFrame(uvm))

    elif cmd[0] == ('split'):
        if type(uvm.splitTuple) is Row:
            uvm.splitTuple.widgets.append(View(uvm))
        else:
            t = uvm.splitTuple
            uvm.splitTuple = Row()
            uvm.splitTuple.widgets.append(t)
            uvm.splitTuple.widgets.append(View(uvm))

    elif cmd[0] == ('vsplit'):
        if type(uvm.splitTuple) is Column:
            uvm.splitTuple.widgets.append(View(uvm))
        t = uvm.splitTuple
        uvm.splitTuple = Column()
        uvm.splitTuple.widgets.append(t)
        uvm.splitTuple.widgets.append(View(uvm))

    elif cmd[0] == ('unsplit'):
        if len(uvm.splitTuple.widgets) > 1:
            uvm.splitTuple.widgets.pop() # doesn't work for mix of split and vsplit

