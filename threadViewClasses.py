#Thread view classes
import time, urwid, re

from bs4 import BeautifulSoup
from customeTypes import VIEWSTYLES
from debug import DEBUG
from customUrwidClasses import QuoteButton

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
                commentWidget = urwid.LineBox(self.commentTagParser(numDate, commentImage[0], images.pop(0)))
            else:
                commentWidget = urwid.LineBox(self.commentTagParser(numDate, commentImage[0]))

            if self.uvm.userFilter:
                if self.uvm.userFilter.lower() in commentImage[0].lower():
                    test.append(commentWidget)
                    temp[str(numDate[0])] = commentWidget
            else:
                test.append(commentWidget)
                temp[str(numDate[0])] = commentWidget

        DEBUG(self.t.postReplyDict)

        endTime = time.time()
        # DEBUG(len(test))
        self.uvm.itemCount = len(self.t.comments)
        self.uvm.parseTime = endTime - startTime

        listbox_content = test
        listbox = urwid.ListBox(urwid.SimpleListWalker(listbox_content))

        return listbox

    def buildThreadView(self):
        listbox = self.getThread()
        # thread = urwid.Overlay(urwid.LineBox(urwid.Pile([listbox])), self.uvm.indexView, 'center', ('relative', 60), 'middle', ('relative', 95))
        self.uvm.bodyView = urwid.Overlay(urwid.LineBox(urwid.Pile([listbox])), self.uvm.indexView, 'center', ('relative', 60), 'middle', ('relative', 95))
        # self.uvm.frame = urwid.Frame(urwid.AttrWrap(thread, 'body'), header=self.header)

    def commentTagParser(self, postNumDate, comment, imageURL=None):
        soup = BeautifulSoup(comment, "html.parser")
        tags = [str(tag) for tag in soup.find_all()]
        contents = []

        test = re.split('<|>', comment)

        contents.append(urwid.Text(str(postNumDate)))
        contents.append(urwid.Divider('-'))

        quote = False
        comment = False
        codeBlock = False
        inlineCode = []

        for item in test:
            with open('log.txt', 'a+') as out:
                out.write(item + '\n')

            # item = item.encode('utf-8', 'xmlcharrefreplace').decode()
            # item = bytes(item, "utf-8").decode()
            # item = item.encode('utf-8')
            # item = ascii(item)
            if len(item) < 1:
                continue
            if '/pre' in item:
                codeBlock = False
                contents.append(urwid.LineBox(urwid.Pile(inlineCode)))
                inlineCode = []
            elif item[0] == '/' and not codeBlock:
                continue
            elif item == 'br':
                continue
            elif 'a href=' in item:
                quote = True
                continue
            elif quote:
                item = item.replace('&#039;', "'")
                item = item.replace('&quot;', '"')
                item = item.replace('&amp;', '&')
                item = item.replace('&gt;', '>')
                item = item.replace('&lt;', '<')

                if str(self.t.currentThreadOPNumber) == item[2:]:
                    item += '(OP)'

                self.t.postReplyDict[item[2:].split('(')[0]].append(str(postNumDate[0]))

                contents.append(urwid.AttrWrap(QuoteButton(item), 'quote'))
                quote = False
            elif 'span class="quote' in item:
                comment = True
                continue
            elif comment:
                item = item.replace('&#039;', "'")
                item = item.replace('&quot;', '"')
                item = item.replace('&amp;', '&')
                item = item.replace('&gt;', '>')
                item = item.replace('&lt;', '<')
                item = item.replace('\r', '\n')

                contents.append(urwid.AttrWrap(urwid.Text(item), 'greenText'))
                comment = False
            elif 'pre class="prettyprint"' in item:
                codeBlock = True
            else:
                item = item.replace('&#039;', "'")
                item = item.replace('&quot;', '"')
                item = item.replace('&amp;', '&')
                item = item.replace('&gt;', '>')
                item = item.replace('&lt;', '<')

                if not codeBlock:
                    contents.append(urwid.Text(item))
                else:
                    inlineCode.append(urwid.Text(item))

        contents.append(urwid.Divider())
        contents.append(urwid.Divider('-'))

        if imageURL:
            contents.append(urwid.Text('Image: ' + str(imageURL)))
        else:
            contents.append(urwid.Text('Image: '))

        contents.append(urwid.Text('Replies: ' + str(self.t.postReplyDict[str(postNumDate[0])])))

        return urwid.Pile(contents)
