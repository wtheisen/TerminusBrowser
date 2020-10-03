from views.view_class import View

from frames.default_frame import FrameFactory
from frames.hackernews.story_frame import StoryFrame
from frames.hackernews.thread_frame import HackerNewsThreadFrame

import logging
log = logging.getLogger(__name__)

HNCommandList = [
    'story',
    'hnp'
]

def hnCommands(cmd, uvm):
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
    uvm.currFocusView.updateHistory(FrameFactory(HackerNewsThreadFrame), [story, postID, uvm])
    setattr(uvm.currFocusView, 'frame', HackerNewsThreadFrame(story, postID, uvm))
