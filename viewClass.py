import urwid

from customeTypes import LEVEL, SITE
from Frames.defaultFrame import DefaultFrame

class View(urwid.WidgetWrap):
    def __init__(self, urwidViewManager, frame=None, uFilter=None):
        self.level = LEVEL.INDEX
        self.site = None
        self.uvm = urwidViewManager
        self.uFilter = uFilter

        if not frame:
            self.frame = DefaultFrame()
        else:
            self.frame = frame

        self.contents = urwid.LineBox(self.frame)
        urwid.WidgetWrap.__init__(self, self.contents)

    def gotFocus(self):
        self.uvm.buildAddHeaderView(self)
        self.uvm.buildAddFooterView(self)
        self.uvm.renderScreen()
