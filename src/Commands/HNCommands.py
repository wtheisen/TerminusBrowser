from debug import DEBUG
from Views.viewClass import View

from Frames.defaultFrame import FrameFactory
from Frames.hackernews.storyFrame import StoryFrame
from Frames.hackernews.threadFrame import HackerNewsThreadFrame

HNCommandList = [
    'story',
    'hnp'
]

def hnCommands(cmd, uvm):
    cmd = cmd.split()
    DEBUG(cmd)

    if cmd[0] == 'story':
        DEBUG('executing story command')
        DEBUG(cmd[0] + cmd[1])
        story(uvm, cmd[1], cmd[2] if len(cmd) == 3 else "")
    elif cmd[0] == 'hnp':
        DEBUG('executing post command')
        hnpost(uvm, cmd[1], cmd[2])

def story(uvm, story, page):
    try:
        setattr(uvm.currFocusView, 'frame', StoryFrame(story, page, uvm))
        uvm.currFocusView.updateHistory(FrameFactory(StoryFrame), [story, page, uvm])
    except:
        uvm.currFocusView.frame.headerString = f'Error connecting to story {story}, does it exist?'
        DEBUG(f'Error connecting to story {story}, does it exist?')

def hnpost(uvm, story, postID):
    DEBUG('Executing HN post command')
    uvm.currFocusView.updateHistory(FrameFactory(HackerNewsThreadFrame), [story, postID, uvm])
    setattr(uvm.currFocusView, 'frame', HackerNewsThreadFrame(story, postID, uvm))