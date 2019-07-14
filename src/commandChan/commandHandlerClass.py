import urwid

from commandChan import commands

from commandChan.debug import DEBUG
from commandChan.customeTypes import SITE

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
        if cmd[0] in ('reddit', '4chan'):
            DEBUG('executing site command')
            self.uvm.site = SITE.REDDIT if cmd[0] == 'reddit' else SITE.FCHAN
            commands.site(self.uvm)
