#Board Meta-class
import requests, collections, json, time

from viewStyles import VIEWSTYLES
from boardViewClasses import buildView
from debug import DEBUG

class Board:
    def __init__(self, board, userFilter, indexView=None):
        self.board = board
        self.userFilter = userFilter
        self.indexView = indexView

        self.threads = {}
        self.style = VIEWSTYLES.BOXES
        self.url = 'https://a.4cdn.org' + board + 'catalog.json'

        startTime = time.time()
        self.titles = self.getJSONCatalog(self.url)
        endTime = time.time()

        DEBUG(self.titles)

        self.parseTime = (endTime - startTime)
        self.itemCount = len(self.titles)

        self.boardView = buildView(self.style,
                                   self.board,
                                   self.titles,
                                   self.userFilter,
                                   self.indexView)

    def getJSONCatalog(self, url):
        response = requests.get(url)
        data = response.json()

        return self.parseFourCatalog(data)

    def parseFourCatalog(self, data):
        titles = collections.OrderedDict()
        for i in range(0, 10):
            page = data[i]
            threadsList = page["threads"]
            for j in range(0, len(threadsList)):
                titles[threadsList[j]["semantic_url"]] = (threadsList[j]["no"], threadsList[j]["replies"], threadsList[j]["images"])
        return titles
