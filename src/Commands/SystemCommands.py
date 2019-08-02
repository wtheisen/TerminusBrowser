import sys

from debug import DEBUG
from customeTypes import SITE
from Views.viewClass import View

from Frames.reddit.indexFrame import RedditIndexFrame
from Frames.fchan.indexFrame import IndexFrame
from Frames.fchan.boardFrame import BoardFrame
from Frames.fchan.threadFrame import ThreadFrame

from splitTracker import Row, Column

SystemCommandList = [
    's', 'search',
    'r', 'refresh',
    'split',
    'vsplit',
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

    elif cmd[0] in ('h', 'history'):
        for h in uvm.history[1:]:
            if h[0] is uvm.currFocusView.id:
                DEBUG('Executing history command')
                uvm.history.insert(0, h)
                setattr(uvm.currFocusView, 'frame', h[1](h[2]))
                break

    elif cmd[0] in ('s', 'search'):
        h = uvm.history[0]
        DEBUG(uvm.history)
        newArgs = h[2].copy()
        if len(cmd) is 2:
            newArgs.append(cmd[1])

        setattr(uvm.currFocusView, 'frame', h[1](newArgs))

    elif cmd[0] in ('view'):
        DEBUG('executing site command')
        DEBUG(cmd)
        if cmd[1] in '4chan':
            DEBUG('4chan requested')
            setattr(uvm.currFocusView, 'site', SITE.FCHAN)
            setattr(uvm.currFocusView, 'boardList', uvm.cfg.get('FCHAN')['boards'])
            uvm.currFocusView.updateHistory(IndexFrame.IndexFrameFactory, [uvm])
            setattr(uvm.currFocusView, 'frame', IndexFrame(uvm))
        elif cmd[1] in ['reddit', 'Reddit']:
            setattr(uvm.currFocusView, 'site', SITE.REDDIT)
            setattr(uvm.currFocusView, 'boardList', uvm.cfg.get('REDDIT')['boards'])
            setattr(uvm.currFocusView, 'frame', RedditIndexFrame(uvm))

    elif cmd[0] in ('split'):
        if type(uvm.splitTuple) is Row:
            uvm.splitTuple.widgets.append(View(uvm))
        else:
            t = uvm.splitTuple
            uvm.splitTuple = Row()
            uvm.splitTuple.widgets.append(t)
            uvm.splitTuple.widgets.append(View(uvm))
        pass
    elif cmd[0] in ('vsplit'):
        if type(uvm.splitTuple) is Column:
            uvm.splitTuple.widgets.append(View(uvm))
        t = uvm.splitTuple
        uvm.splitTuple = Column()
        uvm.splitTuple.widgets.append(t)
        uvm.splitTuple.widgets.append(View(uvm))
