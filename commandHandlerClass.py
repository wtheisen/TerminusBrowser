import urwid

from debug import DEBUG

class CommandHandler:
    def __init__(self, urwidViewManager):
        self.defLeadChar = ':'
        self.uvm = urwidViewManager

    def evalCommand(self, cmd):
        DEBUG(cmd)

        if cmd.split()[0] in ('s' or 'search'):
            self.uvm.userFilter = cmd.split()[1]
            self.uvm.filterUpdate()