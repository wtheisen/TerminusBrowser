from debug import DEBUG
from viewClass import View

from Frames.reddit.subredditFrame import SubredditFrame
from Frames.reddit.threadFrame import RedditThreadFrame

def redditCommands(cmd, uvm):
    cmd = cmd.split()

    if cmd[0] in ('sub', 'subreddit'):
        DEBUG('executing subreddit command')
        subreddit(uvm, cmd[1])
    if cmd[0] in ('p', 'post'):
        DEBUG('executing post command')
        post(uvm, cmd[1], cmd[2])

def subreddit(uvm, subString):
    DEBUG('Executing subreddit command')
    setattr(uvm.currFocusView, 'frame', SubredditFrame(subString, uvm))

def post(uvm, subString, postNumber):
    DEBUG('Executing post command')
    setattr(uvm.currFocusView, 'frame', RedditThreadFrame(subString, postNumber, uvm))
