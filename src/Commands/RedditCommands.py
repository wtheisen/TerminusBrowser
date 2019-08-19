from Views.viewClass import View

from Frames.defaultFrame import FrameFactory
from Frames.reddit.subredditFrame import SubredditFrame
from Frames.reddit.threadFrame import RedditThreadFrame

import logging
log = logging.getLogger(__name__)

RedditCommandList = [
    'sub', 'subreddit',
    'p', 'post'
]

def redditCommands(cmd, uvm):
    log.debug(cmd)
    cmd, *args = cmd.split()

    if cmd in ('sub', 'subreddit') and len(args) >= 1:
        log.debug('executing subreddit command')
        subreddit(uvm, args[0], args[1] if len(args) == 2 else "")
    elif cmd in ('p', 'post') and len(args) == 2:
        log.debug('executing post command')
        post(uvm, args[0], args[1])

def subreddit(uvm, subString, token):
    log.debug('Executing subreddit command')
    subString = '/r/' + subString if not subString.startswith('/r/') else subString
    try:
        setattr(uvm.currFocusView, 'frame', SubredditFrame(subString, token, uvm))
        uvm.currFocusView.updateHistory(FrameFactory(SubredditFrame), [subString, token, uvm])
    except:
        uvm.currFocusView.frame.headerString = f'Error connecting to subreddit {subString}, does it exist?'
        log.debug(f'Error connecting to subreddit {subString}, does it exist?')

def post(uvm, subString, postNumber):
    log.debug('Executing post command')
    uvm.currFocusView.updateHistory(FrameFactory(RedditThreadFrame), [subString, postNumber, uvm])
    setattr(uvm.currFocusView, 'frame', RedditThreadFrame(subString, postNumber, uvm))
