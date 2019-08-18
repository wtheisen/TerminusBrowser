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

def redditCommands(cmd, args, uvm):

    if cmd[0] in ('sub', 'subreddit'):
        log.debug('executing subreddit command')
        subreddit(uvm, cmd[1], cmd[2] if len(cmd) == 3 else "")
    elif cmd[0] in ('p', 'post'):
        log.debug('executing post command')
        post(uvm, cmd[1], cmd[2])

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
