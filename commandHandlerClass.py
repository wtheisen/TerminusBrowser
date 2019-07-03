import urwid

from debug import DEBUG

class CommandHandler:
    def __init__(self):
        self.defLeadChar = ':'

    def evalCommand(self, cmd):
        DEBUG(cmd)