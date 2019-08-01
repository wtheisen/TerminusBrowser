from debug import DEBUG
from Views.viewClass import View

from Frames.reddit.subredditFrame import SubredditFrame
from Frames.reddit.threadFrame import RedditThreadFrame

def redditCommands(cmd, uvm):
    cmd = cmd.split()

    if cmd[0] in ('sub', 'subreddit'):
        DEBUG('executing subreddit command')
        subreddit(uvm, cmd[1])
    elif cmd[0] in ('p', 'post'):
        DEBUG('executing post command')
        post(uvm, cmd[1], cmd[2])
    elif cmd[0] in ('subpage'):
        DEBUG('executing url command')
        subredditpage(uvm, cmd[1], cmd[2])

def subreddit(uvm, subString):
    DEBUG('Executing subreddit command')
    setattr(uvm.currFocusView, 'frame', SubredditFrame(subString, uvm))

def post(uvm, subString, postNumber):
    DEBUG('Executing post command')
    setattr(uvm.currFocusView, 'frame', RedditThreadFrame(subString, postNumber, uvm))

def subredditpage(uvm, subString, token):
    DEBUG('Executing sub page command')
    setattr(uvm.currFocusView, 'frame', SubredditFrame(subString, uvm, token=token))
