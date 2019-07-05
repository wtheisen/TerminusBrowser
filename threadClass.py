#Thread Class
import requests, json, collections, re
import urwid

from bs4 import BeautifulSoup
from debug import DEBUG
from threadViewClasses import buildView
from customeTypes import VIEWSTYLES

class Thread:
    def __init__(self, urwidViewManager):
        self.uvm = urwidViewManager
        self.url = 'https://a.4cdn.org' + self.uvm.boardString + 'thread/' + str(self.uvm.threadNum)
        self.imageUrl = 'http://boards.4chan.org' + self.uvm.boardString + 'thread/' + str(self.uvm.threadNum)

        self.postReplyDict = {}

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

        for post in posts:
            self.postReplyDict[str(post["no"])] = []

            if str(post["resto"]) == '0':
                self.currentThreadOPNumber = str(post["no"])
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


