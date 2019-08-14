from Views.viewClass import View

from Frames.defaultFrame import FrameFactory
from Frames.hackernews.storyFrame import StoryFrame
from Frames.hackernews.threadFrame import HackerNewsThreadFrame

import logging
log = logging.getLogger(__name__)

HNCommandList = [
    'story',
    'hnp'
]

def hnCommands(cmd, uvm):
    cmd = cmd.split()
    log.debug(cmd)

    if cmd[0] == 'story':

        log.debug('executing story command')
        log.debug(cmd[0] + cmd[1])
        story(uvm, cmd[1], cmd[2] if len(cmd) == 3 else "")
    elif cmd[0] == 'hnp':
        log.debug('executing post command')
        hnpost(uvm, cmd[1], cmd[2])

def story(uvm, story, page):
    try:
        setattr(uvm.currFocusView, 'frame', StoryFrame(story, page, uvm))
        uvm.currFocusView.updateHistory(FrameFactory(StoryFrame), [story, page, uvm])
    except:
        uvm.currFocusView.frame.headerString = f'Error connecting to story {story}, does it exist?'
        log.debug(f'Error connecting to story {story}, does it exist?')

def hnpost(uvm, story, postID):
    log.debug('Executing HN post command')
    uvm.currFocusView.updateHistory(FrameFactory(HackerNewsThreadFrame), [story, postID, uvm])
    setattr(uvm.currFocusView, 'frame', HackerNewsThreadFrame(story, postID, uvm))