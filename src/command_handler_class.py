import urwid, sys

from commands.system_commands import systemCommands, SystemCommandList
from commands.chan_commands import chanCommands, ChanCommandList
from commands.reddit_commands import redditCommands, RedditCommandList
from commands.hn_commands import hnCommands, HNCommandList
from commands.lobster_commands import lobsterCommands, LobsterCommandList

from customer_types import SITE, MODE

import logging
log = logging.getLogger(__name__)

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

        log.debug(cmd)

        if cmd.split()[0] not in (SystemCommandList + ChanCommandList + RedditCommandList + HNCommandList + LobsterCommandList):
            return
        elif cmd.split()[0] in SystemCommandList:
            systemCommands(cmd, self.uvm)
        elif cmd.split()[0] in ChanCommandList:
            chanCommands(cmd, self.uvm)
        elif cmd.split()[0] in RedditCommandList:
            redditCommands(cmd, self.uvm)
        elif cmd.split()[0] in HNCommandList:
            hnCommands(cmd, self.uvm)
        elif cmd.split()[0] in LobsterCommandList:
            lobsterCommands(cmd, self.uvm)

        self.postCommand()
