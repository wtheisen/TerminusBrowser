import urwid

from customer_types import LEVEL, SITE
from frames.default_frame import DefaultFrame

class View(urwid.WidgetWrap):
    def __init__(self, urwidViewManager, frame=None, uFilter=None):
        self.level = LEVEL.INDEX
        self.site = None
        self.uvm = urwidViewManager
        self.uFilter = uFilter
        self.id = self.uvm.getFreeID()

        if not frame:
            self.frame = DefaultFrame()
        else:
            self.frame = frame

    def updateHistory(self, classPointer, args):
        self.uvm.history.insert(0, (self.id, classPointer, args))
