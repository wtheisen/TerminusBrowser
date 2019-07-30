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

        if cmd.split()[0] in SystemCommandList:
            systemCommands(cmd, self.uvm)

        if self.uvm.currFocusView.site is SITE.FCHAN:
            chanCommands(cmd, self.uvm)
        if self.uvm.currFocusView.site is SITE.REDDIT:
            redditCommands(cmd, self.uvm)

        self.postCommand()


        # if cmd[0] in ('qa', 'quitall'):
        #     DEBUG('executing quit command')
        #     sys.exit()
        # if cmd[0] in ('s', 'search'):
        #     DEBUG('executing search command')
        #     commands.search(self.uvm, cmd[1] if len(cmd) is 2 else None)
        # if cmd[0] in ('b', 'board'):
        #     DEBUG('executing board command')
        #     commands.board(self.uvm, cmd[1])
        # if cmd[0] in ('t', 'thread'):
        #     DEBUG('executing thread command')
        #     commands.thread(self.uvm, cmd[1])
        # if cmd[0] in ('h', 'history'):
        #     DEBUG('executing history command')
        #     commands.history(self.uvm)
        # if cmd[0] in ('reddit', '4chan'):
        #     DEBUG('executing site command')
        #     self.uvm.site = SITE.REDDIT if cmd[0] == 'reddit' else SITE.FCHAN
        #     commands.site(self.uvm)
        # if cmd[0] == 'stickies':
        #    self.uvm.stickies = STICKIES.HIDE if self.uvm.stickies == STICKIES.SHOW else STICKIES.SHOW
        #    commands.refresh(self.uvm)
        # if cmd[0] == 'split':
        #     commands.split(self.uvm, 0, None)
        # if cmd[0] == 'vsplit':
        #     commands.split(self.uvm, 1, None)
