import urwid, requests, re

from html import unescape
from html.parser import HTMLParser

from customUrwidClasses import QuoteButton

from postClass import Post

class ChanThreadBuilder():
    def getJSONThread(self):
        response = requests.get(self.url, headers=self.headers)
        data = response.json()
        return self.parseFourThread(data)

    def parseFourThread(self, data):
        commentObjList = []
        posts = data["posts"]

        for post in posts:
            if str(post["resto"]) == '0':
                self.currentThreadOPNumber = str(post["no"])

            p = Post(
                str(post['no']),
                post['com'] if 'com' in post else "",
                post['now'] if 'now' in post else post['time'],
                self.imgPrefix + self.boardString + str(post["tim"]) + post["ext"] if 'ext' in post else ''
            )

            commentObjList.append(p)

        return commentObjList

    def buildFrame(self):
        listbox = self.buildThread()
        return urwid.Pile([listbox])

    def buildThread(self):
        self.postWidgetDict = {}

        for p in self.comments:
            self.postReplyDict[str(p.userIden)] = []

            commentWidget = self.notBrainletCommentTagParser(p)

            if self.uFilter:
                if self.uFilter.lower() in p.content.lower():
                    self.postWidgetDict[p.userIden] = commentWidget
            else:
                self.postWidgetDict[p.userIden] = commentWidget

        postWidgetList = []
        for pNum, pWidget in self.postWidgetDict.items():
            if pNum in self.postReplyDict:
                pWidget.append(urwid.Text('Replies: ' + str(self.postReplyDict[pNum])))
            postWidgetList.append(urwid.LineBox(urwid.Pile(pWidget)))

        self.parsedItems = len(self.comments)


        listbox_content = postWidgetList
        listbox = urwid.ListBox(urwid.SimpleListWalker(listbox_content))

        return listbox

    def notBrainletCommentTagParser(self, post):
        widgetContent = []
        rawCommentText = post.content
        unescape(rawCommentText)
        parent = self

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

                    widgetContent.append(urwid.AttrWrap(QuoteButton(str(data), parent.uvm), 'quote'))
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
