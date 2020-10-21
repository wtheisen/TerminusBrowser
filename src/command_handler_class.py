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
                log.debug(f"command does not exist {e}")
            else:
                command_scope(cmd, self.uvm)

        self.postCommand()
