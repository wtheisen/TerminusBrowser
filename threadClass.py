#Thread Class
import requests, json, collections, re
import urwid

from bs4 import BeautifulSoup
from customUrwidClasses import QuoteButton
from debug import DEBUG
from threadViewClasses import buildView
from viewStyles import VIEWSTYLES

class Thread:
    def __init__(self, urwidViewManager):
        self.uvm = urwidViewManager
        self.url = 'https://a.4cdn.org' + self.uvm.boardString + 'thread/' + str(self.uvm.threadNum)
        self.imageUrl = 'http://boards.4chan.org' + self.uvm.boardString + 'thread/' + str(self.uvm.threadNum)

        self.comments = self.getJSONThread()
        # DEBUG(self.comments)
        self.getImageUrls()

        buildView(VIEWSTYLES.BOXES, self.uvm, self)


    def getJSONThread(self):
        response = requests.get(self.url + '.json')
        data = response.json()
        return self.parseFourThread(data)

    def parseFourThread(self, data):
        comments = collections.OrderedDict()
        posts = data["posts"]

        replies = {}
        for post in posts:
            if str(post["resto"]) == '0':
                self.currentThreadOPNumber = str(post["no"])

            replies[str(post["no"])] = []
            try:
                comStr = BeautifulSoup(post["com"], 'lxml')
                quotes = comStr.find('a')
                quotes = quotes.attrs['href']
                replies += quotes
            except:
                pass

            try:
                imageBool = post['filename']
                try:
                    comments[(str(post["no"]), post["now"])] = (post["com"], True)
                except:
                    comments[(str(post["no"]), post["now"])] = ('', True)
            except:
                try:
                    comments[(str(post["no"]), post["now"])] = (post["com"], False)
                except:
                    comments[(str(post["no"]), post["now"])] = ('', False)
        return comments

    def getImageUrls(self):
        def load(url):
            req = requests.get(url)
            return str(req.content)

        DEBUG(self.url)
        page = BeautifulSoup(load(self.imageUrl), "lxml")
        # DEBUG(page)
        extensionList = ('.jpg', '.jpeg', '.png', '.gif', '.webm')
        images = []

        for img in page.find_all('a', href=True):
            if self.uvm.boardString in str(img) and 'i.4cdn.org' in str(img):
                tagList = str(img).split('"')
                for tag in tagList:
                    if self.uvm.boardString in str(tag):
                        if any(extension in tag for extension in extensionList):
                            images.append(str(tag))

        DEBUG(images)
        self.images = images

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

                if str(self.currentThreadOPNumber) == item[2:]:
                    item += '(OP)'

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

        contents.append(urwid.Text('Replies: '))

        return urwid.Pile(contents)
