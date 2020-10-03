import urwid, sys

from Commands.SystemCommands import systemCommands, SystemCommandList
from Commands.ChanCommands import chanCommands, ChanCommandList
from Commands.RedditCommands import redditCommands, RedditCommandList
from Commands.HNCommands import hnCommands, HNCommandList
from Commands.LobsterCommands import lobsterCommands, LobsterCommandList

from customeTypes import SITE, MODE

import logging
log = logging.getLogger(__name__)


class CommandHandler:
    command_map = {
        str(SITE.REDDIT): redditCommands,
        str(SITE.FCHAN): chanCommands,
        str(SITE.LCHAN): chanCommands,
        str(SITE.HACKERNEWS): hnCommands,
        str(SITE.LOBSTERS): lobsterCommands,
    }

    command_set = set(SystemCommandList + ChanCommandList + RedditCommandList + HNCommandList + LobsterCommandList)

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

        if cmd.split()[0] not in self.command_set:
            return
        elif cmd.split()[0] in SystemCommandList:
            systemCommands(cmd, self.uvm)
        else:
            try:
                command_scope = self.command_map[str(self.uvm.currFocusView.site)]
            except KeyError as e:
                log.debug("command does not exist {e}")
            else:
                command_scope(cmd, self.uvm)

        self.postCommand()
