#Thread Class
import requests, json, collections, re
import urwid

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
        # self.getImageUrls()

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
            # try:
            #     comStr = BeautifulSoup(post["com"], 'lxml')
            #     quotes = comStr.find('a')
            #     quotes = quotes.attrs['href']
            #     replies += quotes
            # except:
            #     pass

            try:
                imageBool = post['filename']
                try:
                    comments[(str(post["no"]), post["now"])] = (post["com"], 'https://i.4cdn.org' + self.uvm.boardString + str(post["tim"]) + post["ext"])
                    DEBUG('Added an image')
                except:
                    comments[(str(post["no"]), post["now"])] = ('', 'https://i.4cdn.org' + self.uvm.boardString + str(post["tim"]) + post["ext"])
            except:
                try:
                    comments[(str(post["no"]), post["now"])] = (post["com"], '')
                except:
                    comments[(str(post["no"]), post["now"])] = ('', '')
        return comments
