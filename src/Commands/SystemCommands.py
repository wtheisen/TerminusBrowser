import sys
import os

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
    log.debug(cmd)
    cmd, *args = cmd.split()
    
    
    if cmd in ('q', 'qa', 'quitall'):
        log.debug('Executing quit command')
        if uvm.cfg.update_file():
            log.debug('updated config')
        sys.exit()

    elif cmd == ('add'):
        if len(args) >= 2:
            log.debug(f'Executing add command with args: {args[:]}')
            if args[0] == '4chan':
                for board in args[1:]:
                    uvm.cfg.add_topic(SITE.FCHAN, board)
                    setattr(uvm.currFocusView, 'frame', fIndex.IndexFrame(uvm))
            elif args[0] == 'reddit':
                for subreddit in args[1:]:
                    uvm.cfg.add_topic(SITE.REDDIT, subreddit)
                    setattr(uvm.currFocusView, 'frame', RedditIndexFrame(uvm))

    elif cmd == ('set'):
        # :set key value
        log.debug('set called')
        if len(args) == 2:
            uvm.cfg.set(args[0], args[1])
        # :set SITE key value
        elif len(args) == 3:
            uvm.cfg.deep_set(args[0], args[1], args[2])

    elif cmd == ('source') and len(args) == 1:
        try:
            if(os.path.exists(args[0])):
                with open(args[0], 'r') as rcFile:
                    for command in rcFile:
                        command = command.strip()
                        if command[0] != '#':
                            systemCommands(command, uvm)
        except:
            log.debug(f'ERROR: Unable to source {args[0]}')

    elif cmd in ('h', 'history'):
        if len(args) == 1:
            try:
                val = int(args[0])
                h = uvm.history[val]
                setattr(uvm.currFocusView, 'frame', h[1](h[2]))
            except ValueError:
                log.error('tried feeding string, instead of int to history')
                
        else:
            for h in uvm.history[1:]:
                if h[0] is uvm.currFocusView.id:
                    log.debug('Executing history command')
                    uvm.history.insert(0, h)
                    setattr(uvm.currFocusView, 'frame', h[1](h[2]))
                    break

    elif cmd in ('s', 'search'):
        h = uvm.history[0]
        newArgs = h[2].copy()
        if len(args) == 1:
            newArgs.append(args[0])

        setattr(uvm.currFocusView, 'frame', h[1](newArgs))

    elif cmd == ('view'):
        log.debug('executing view command')
        log.debug(cmd)
        if len(args) == 1:
            if args[0].lower() in ('h', 'history'):
                log.debug('history requested')
                setattr(uvm.currFocusView, 'frame', HistoryFrame(uvm))
            elif args[0].lower() in '4chan':
                log.debug('4chan requested')
                uvm.currFocusView.updateHistory(FrameFactory(fIndex.IndexFrame), [uvm])
                setattr(uvm.currFocusView, 'frame', fIndex.IndexFrame(uvm))
            elif args[0].lower() in ('lchan', 'lainchan'):
                log.debug('lainchan requested')
                uvm.currFocusView.updateHistory(FrameFactory(lIndex.IndexFrame), [uvm])
                setattr(uvm.currFocusView, 'frame', lIndex.IndexFrame(uvm))
            elif args[0].lower() in 'reddit':
                log.debug('reddit requested')
                uvm.currFocusView.updateHistory(FrameFactory(RedditIndexFrame), [uvm])
                setattr(uvm.currFocusView, 'frame', RedditIndexFrame(uvm))
            elif args[0].lower() in ('hn', 'hackernews'):
                log.debug('HN requested')
                uvm.currFocusView.updateHistory(FrameFactory(HackerNewsIndexFrame), [uvm])
                setattr(uvm.currFocusView, 'frame', HackerNewsIndexFrame(uvm))
            elif args[0].lower() in 'watcher':
                log.debug('wather requested')
                # setattr(uvm.currFocusView, 'frame', WatcherFrame(uvm))

    elif cmd == ('split'):
        if type(uvm.splitTuple) is Row:
            uvm.splitTuple.widgets.append(View(uvm))
        else:
            t = uvm.splitTuple
            uvm.splitTuple = Row()
            uvm.splitTuple.widgets.append(t)
            uvm.splitTuple.widgets.append(View(uvm))

    elif cmd == ('vsplit'):
        if type(uvm.splitTuple) is Column:
            uvm.splitTuple.widgets.append(View(uvm))
        t = uvm.splitTuple
        uvm.splitTuple = Column()
        uvm.splitTuple.widgets.append(t)
        uvm.splitTuple.widgets.append(View(uvm))

    elif cmd == ('unsplit'):
        if len(uvm.splitTuple.widgets) > 1:
            uvm.splitTuple.widgets.pop() # doesn't work for mix of split and vsplit

    elif cmd == ('watch'):
        uvm.watched.add(uvm.currFocusView.threadNumber)
