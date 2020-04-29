from Views.viewClass import View

from Frames.defaultFrame import FrameFactory
from Frames.lobster.storyFrame import StoryFrame
from Frames.lobster.threadFrame import LobsterThreadFrame

import logging
log = logging.getLogger(__name__)

LobsterCommandList = [
    'lstory',
    'lp'
]

def lobsterCommands(cmd, uvm):
    log.debug(cmd)
    cmd, *args = cmd.split()

    if cmd == 'story' and len(args) >= 2:
        log.debug('executing story command')
        log.debug(cmd + args[0])
        story(uvm, args[0], args[1] if len(args) == 2 else "")
    elif cmd == 'hnp' and len(args) == 2:
        log.debug('executing post command')
        hnpost(uvm, args[0], args[1])

def story(uvm, story, page):
    try:
        setattr(uvm.currFocusView, 'frame', StoryFrame(story, page, uvm))
        uvm.currFocusView.updateHistory(FrameFactory(StoryFrame), [story, page, uvm])
    except:
        uvm.currFocusView.frame.headerString = f'Error connecting to story {story}, does it exist?'
        log.debug(f'Error connecting to story {story}, does it exist?')

def hnpost(uvm, story, postID):
    log.debug('Executing HN post command')
    uvm.currFocusView.updateHistory(FrameFactory(LobsterThreadFrame), [story, postID, uvm])
    setattr(uvm.currFocusView, 'frame', LobsterThreadFrame(story, postID, uvm))
