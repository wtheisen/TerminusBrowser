import urwid, sys

from Commands.SystemCommands import SystemCommandList, systemCommands
from Commands.ChanCommands import chanCommands
from Commands.RedditCommands import redditCommands

from debug import DEBUG
from customeTypes import SITE, MODE

class CommandHandler:
    def __init__(self, uvm):
        self.defLeadChar = ':'
        self.uvm = uvm

    def preCommand(self):
        self.uvm.commandBar.set_caption('')
        self.uvm.mode = MODE.NORMAL
        self.uvm.body.focus_position = 'body'

    def postCommand(self):
        self.uvm.buildAddHeaderView(self.uvm.currFocusView)
        self.uvm.buildAddFooterView(self.uvm.currFocusView)
        self.uvm.renderScreen()

    def routeCommand(self, cmd):
        self.preCommand()

        DEBUG(cmd)
        if cmd.split()[0] in SystemCommandList:
            # if matched return
            if systemCommands(cmd, self.uvm):
                self.postCommand()
                return

        DEBUG(self.uvm.site)
        if self.uvm.currFocusView.site is SITE.FCHAN:
            chanCommands(cmd, self.uvm)
        if self.uvm.currFocusView.site is SITE.REDDIT:
            redditCommands(cmd, self.uvm)

        self.postCommand()
