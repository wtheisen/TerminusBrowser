import sys

from debug import DEBUG
from customeTypes import SITE
from viewClass import View

from Frames.reddit.indexFrame import RedditIndexFrame
from Frames.fchan.indexFrame import IndexFrame

from splitTracker import Row, Column

SystemCommandList = [
    'search',
    'refresh',
    'split',
    'vsplit',
    'site',
    'history'
    'q',
    'qa',
    'quitall'
]

def systemCommands(cmd, uvm):
    cmd = cmd.split()

    if cmd[0] in ('qa', 'quitall'):
        DEBUG('Executing quit command')
        sys.exit()

    if cmd[0] in ('site'):
        DEBUG('executing site command')
        DEBUG(cmd)
        if cmd[1] in '4chan':
            DEBUG('4chan requested')
            setattr(uvm.currFocusView, 'site', SITE.FCHAN)
            setattr(uvm.currFocusView, 'boardList', uvm.cfg.get('FCHAN')['boards'])
            setattr(uvm.currFocusView, 'frame', IndexFrame(uvm))
        elif cmd[1] in ['reddit', 'Reddit']:
            setattr(uvm.currFocusView, 'site', SITE.REDDIT)
            setattr(uvm.currFocusView, 'boardList', uvm.cfg.get('REDDIT')['boards'])
            setattr(uvm.currFocusView, 'frame', RedditIndexFrame(uvm))

    if cmd[0] in ('split'):
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
