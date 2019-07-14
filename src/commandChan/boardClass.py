#Board Meta-class
import requests, collections, json, time

from commandChan.customeTypes import VIEWSTYLES, SITE
from commandChan.boardViewClasses import buildView
from commandChan.debug import DEBUG

class Board:
    def __init__(self, urwidViewManager):
        self.uvm = urwidViewManager

        self.threadNums = []
        self.style = VIEWSTYLES.BOXES
        if self.uvm.site == SITE.FCHAN:
            self.url = 'https://a.4cdn.org' + self.uvm.boardString + 'catalog.json'
            self.headers = {}
        elif self.uvm.site == SITE.REDDIT:
            self.url = 'https://www.reddit.com' + self.uvm.boardString + '.json'
            self.headers = {
                'user-agent': 'reddit-commandChan'
            }
        startTime = time.time()
        self.titles = self.getJSONCatalog(self.url)
        endTime = time.time()

        DEBUG(self.titles)

        self.uvm.parseTime = (endTime - startTime)

        self.boardView = buildView(self.style,
                                   self.uvm,
                                   self)

    def getJSONCatalog(self, url):
        response = requests.get(url, headers=self.headers)
        data = response.json()
       
        if self.uvm.site == SITE.FCHAN:
            return self.parseFourCatalog(data)
        elif self.uvm.site == SITE.REDDIT:
            return self.parseSubreddit(data)
        return collections.OrderedDict()

    def parseFourCatalog(self, data):
        titles = collections.OrderedDict()
        for i in range(0, 10):
            page = data[i]
            threadsList = page["threads"]
            for j in range(0, len(threadsList)):
                titles[threadsList[j]["semantic_url"]] = (threadsList[j]["no"], threadsList[j]["replies"], threadsList[j]["images"])
                self.threadNums.append(threadsList[j]["no"])
        return titles

    def parseSubreddit(self, data):
        titles = collections.OrderedDict()
        posts = data['data']['children']
        
        for post in posts:
            titles[post['data']['title']] = (post['data']['permalink'],
                                             post['data']['score'],
                                             post['data']['subreddit'])
            self.threadNums.append(post['data']['title'])
        return titles
