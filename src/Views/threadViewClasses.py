#Thread view classes
import time, urwid, re

from html import unescape
from html.parser import HTMLParser

from postClass import Post
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
        postWidgetDict = {}

        # images = [ img for img in self.t.images if re.match(r"^//.*/.*/.*s\..*", img) ]
        # DEBUG(images)
        # for i in range(0, len(images)):
        #     images[i] = 'http:' + images[i]

        for p in self.t.comments:
            DEBUG(p.userIden)
            self.t.postReplyDict[str(p.userIden)] = []

            # commentWidget = urwid.LineBox(self.commentTagParser(f'{p.userIden} {p.timestamp}', p.content, p.image))
            # commentWidget = self.commentTagParser(f'{p.userIden} {p.timestamp}', p.content, p.image)
            commentWidget = self.notBrainletCommentTagParser(p)

            if self.uvm.userFilter:
                if self.uvm.userFilter.lower() in p.content.lower():
                    # postWidgetList.append(commentWidget)
                    postWidgetDict[p.userIdent] = commentWidget
            else:
                # test.append(commentWidget)
                postWidgetDict[p.userIden] = commentWidget

        postWidgetList = []
        for pNum, pWidget in postWidgetDict.items():
            if pNum in self.t.postReplyDict:
                pWidget.append(urwid.Text('Replies: ' + str(self.t.postReplyDict[pNum])))
            postWidgetList.append(urwid.LineBox(urwid.Pile(pWidget)))

        DEBUG(self.t.postReplyDict)

        endTime = time.time()
        # DEBUG(len(test))
        self.uvm.itemCount = len(self.t.comments)
        self.uvm.parseTime = endTime - startTime

        listbox_content = postWidgetList
        listbox = urwid.ListBox(urwid.SimpleListWalker(listbox_content))

        return listbox

    def buildThreadView(self):
        listbox = self.getThread()
        # thread = urwid.Overlay(urwid.LineBox(urwid.Pile([listbox])), self.uvm.indexView, 'center', ('relative', 60), 'middle', ('relative', 95))
        self.uvm.bodyView = urwid.Overlay(urwid.LineBox(urwid.Pile([listbox])), self.uvm.indexView, 'center', ('relative', 60), 'middle', ('relative', 95))
        # self.uvm.frame = urwid.Frame(urwid.AttrWrap(thread, 'body'), header=self.header)

    def notBrainletCommentTagParser(self, post):
        widgetContent = []
        rawCommentText = post.content
        unescape(rawCommentText)
        parent = self.t

        class CommentParser(HTMLParser):
            currTag = ''

            def handle_starttag(self, tag, attrs):
                self.currTag = str(tag)

            def handle_endtag(self, tag):
                self.currTag = ''

            def handle_data(self, data):
                if self.currTag == 'span':
                    widgetContent.append(urwid.AttrWrap(urwid.Text(str(data)), 'greenText'))
                elif self.currTag == 'a':
                    if str(parent.currentThreadOPNumber) == data[2:]:
                        data += '(OP)'

                    try:
                        parent.postReplyDict[data[2:].split('(')[0]].append(str(post.userIden))
                    except KeyError:
                        pass

                    widgetContent.append(urwid.AttrWrap(QuoteButton(str(data)), 'quote'))
                else:
                    widgetContent.append(urwid.Text(data))

        p = CommentParser()
        p.feed(rawCommentText)

        widgetContent.append(urwid.Divider())
        widgetContent.append(urwid.Divider('-'))

        if post.image:
            widgetContent.append(urwid.Text('URL: ' + str(post.image)))
        else:
            widgetContent.append(urwid.Text('URL: '))

        return widgetContent