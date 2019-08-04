import sys

from debug import DEBUG
from customeTypes import SITE
from Views.viewClass import View

from Frames.defaultFrame import FrameFactory
from Frames.historyFrame import HistoryFrame
from Frames.reddit.indexFrame import RedditIndexFrame
from Frames.fchan.indexFrame import IndexFrame
from Frames.fchan.boardFrame import BoardFrame
from Frames.fchan.threadFrame import ThreadFrame

from splitTracker import Row, Column

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
        DEBUG('Executing quit command')
        sys.exit()

    elif cmd[0] == ('add'):
        if len(cmd) >= 3:
            DEBUG(f'Executing add command with args: {cmd[1:]}')
            if cmd[1] == '4chan':
                for board in cmd[2:]:
                    uvm.boardList.append(board)
            elif cmd[1] == 'reddit':
                for subreddit in cmd[2:]:
                    uvm.subredditList.append(subreddit)

    elif cmd[0] == ('set'):
        pass

    elif cmd[0] == ('source'):
        pass
        try:
            with open(cmd[1], 'r') as rcFile:
                for command in rcFile:
                    command = command.strip()
                    if command[0] != '#':
                        systemCommands(command, uvm)
        except:
            DEBUG(f'ERROR: Unable to source {cmd[1]}')

    elif cmd[0] in ('h', 'history'):
        if len(cmd) is 2:
            h = uvm.history[int(cmd[1])]
            setattr(uvm.currFocusView, 'frame', h[1](h[2]))
        else:
            for h in uvm.history[1:]:
                if h[0] is uvm.currFocusView.id:
                    DEBUG('Executing history command')
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
        DEBUG('executing site command')
        DEBUG(cmd)
        if len(cmd) == 2:
            if cmd[1] in 'history':
                # setattr(uvm.currFocusView, 'site', SITE.FCHAN)
                # setattr(uvm.currFocusView, 'boardList', uvm.boardList)
                # uvm.currFocusView.updateHistory(IndexFrame.IndexFrameFactory, [uvm])
                setattr(uvm.currFocusView, 'frame', HistoryFrame(uvm))
            elif cmd[1] == '4chan':
                DEBUG('4chan requested')
                setattr(uvm.currFocusView, 'site', SITE.FCHAN)
                # setattr(uvm.currFocusView, 'boardList', uvm.boardList)
                uvm.currFocusView.updateHistory(FrameFactory([uvm], IndexFrame))
                setattr(uvm.currFocusView, 'frame', IndexFrame(uvm))
            elif cmd[1] in ['reddit', 'Reddit']:
                setattr(uvm.currFocusView, 'site', SITE.REDDIT)
                # setattr(uvm.currFocusView, 'boardList', uvm.subredditList)
                uvm.currFocusView.updateHistory(FrameFactory([uvm], RedditIndexFrame))
                setattr(uvm.currFocusView, 'frame', RedditIndexFrame(uvm))

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

