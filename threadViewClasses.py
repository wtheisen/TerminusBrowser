#Thread view classes
import time, urwid, re
from customeTypes import VIEWSTYLES
from debug import DEBUG

def buildView(style, urwidViewManager, thread):
    if style is VIEWSTYLES.BOXES:
        return urwidThreadViewBoxes(urwidViewManager, thread)
   
class urwidThreadViewBoxes:

    def __init__(self, urwidViewManager, thread):
        self.uvm = urwidViewManager
        self.t = thread

        DEBUG('YEET')

        self.buildHeaderView()
        self.buildThreadView()

    def buildHeaderView(self):
            self.header = urwid.AttrWrap(urwid.Text('CommandChan'), 'header')

    def getThread(self):
        startTime = time.time()
        test = []
        temp = {}

        images = [ img for img in self.t.images if re.match(r"^//.*/.*/.*s\..*", img) ]
        DEBUG(images)
        for i in range(0, len(images)):
            images[i] = 'http:' + images[i]

        for numDate, commentImage in self.t.comments.items():
            DEBUG(commentImage)
            if commentImage[1] is True:
                commentWidget = urwid.LineBox(self.t.commentTagParser(numDate, commentImage[0], images.pop(0)))
            else:
                commentWidget = urwid.LineBox(self.t.commentTagParser(numDate, commentImage[0]))

            test.append(commentWidget)
            temp[str(numDate[0])] = commentWidget

        endTime = time.time()
        # DEBUG(len(test))
        self.uvm.itemCount = len(self.t.comments)
        self.uvm.parseTime = endTime - startTime

        listbox_content = test
        listbox = urwid.ListBox(urwid.SimpleListWalker(listbox_content))

        return listbox

    def buildThreadView(self):
        listbox = self.getThread()
        thread = urwid.Overlay(urwid.LineBox(urwid.Pile([listbox])), self.uvm.indexView, 'center', ('relative', 60), 'middle', ('relative', 95))
        self.uvm.frame = urwid.Frame(urwid.AttrWrap(thread, 'body'), header=self.header)