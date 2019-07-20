import urwid

import commands

from debug import DEBUG
from customeTypes import SITE, STICKIES

class CommandHandler:
    def __init__(self, urwidViewManager):
        self.defLeadChar = ':'
        self.uvm = urwidViewManager

    def evalCommand(self, cmd):
        cmd = cmd.split()
        DEBUG(cmd)

        if cmd[0] in ('s', 'search'):
            DEBUG('executing search command')
            if len(cmd) is 1:
                self.uvm.userFilter = None
            elif len(cmd) is 2:
                self.uvm.userFilter = cmd[1]
            commands.search(self.uvm)
        if cmd[0] in ('t', 'thread'):
            DEBUG('executing thread command')
            self.uvm.threadNum = cmd[1]
            commands.thread(self.uvm)
        if cmd[0] in ('h', 'history'):
            DEBUG('executing history command')
            if len(cmd) == 1:
                self.uvm.threadID = self.uvm.history[0]
            else:
                self.uvm.threadID = self.uvm.history[int(cmd[1])]
            commands.thread(self.uvm)
        if cmd[0] in ('reddit', '4chan'):
            DEBUG('executing site command')
            self.uvm.site = SITE.REDDIT if cmd[0] == 'reddit' else SITE.FCHAN
            commands.site(self.uvm)
        if cmd[0] == 'stickies':
           self.uvm.stickies = STICKIES.HIDE if self.uvm.stickies == STICKIES.SHOW else STICKIES.SHOW
           commands.refresh(self.uvm)