import urwid

import commands

from debug import DEBUG

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
