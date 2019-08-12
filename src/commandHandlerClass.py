import urwid, sys

from Commands.SystemCommands import systemCommands, SystemCommandList
from Commands.ChanCommands import chanCommands, ChanCommandList
from Commands.RedditCommands import redditCommands, RedditCommandList
from Commands.HNCommands import hnCommands, HNCommandList

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

        if cmd.split()[0] not in (SystemCommandList + ChanCommandList + RedditCommandList + HNCommandList):
            return
        elif cmd.split()[0] in SystemCommandList:
            systemCommands(cmd, self.uvm)
        elif cmd.split()[0] in ChanCommandList:
            chanCommands(cmd, self.uvm)
        elif cmd.split()[0] in RedditCommandList:
            redditCommands(cmd, self.uvm)
        elif cmd.split()[0] in HNCommandList:
            hnCommands(cmd, self.uvm)

        self.postCommand()
