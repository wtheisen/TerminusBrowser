import urwid
import time

class AbstractFrame(urwid.WidgetWrap):
    def __init__(self, urwidViewManager, uFilter):
        self.uvm = urwidViewManager
        self.uFilter = uFilter
        
        self.footerStringRight = None
        self.contents = None

        # To measure how fast we load in the data
        self.startTime = None
        self.endTime = None
        self.parsedItems = 0

    def loader(self):
        raise NotImplementedError

    def load(self):
        self.startTime = time.time()
        self.loader()
        self.endTime = time.time()
        self.footerStringRight = f'Parsed {self.parsedItems} items in {(self.endTime - self.startTime):.4f}s'

        # self.contents MUST BE SET in self.loader()
        if self.contents == None:
            raise ValueError(object)
        
        urwid.WidgetWrap.__init__(self, self.contents)
