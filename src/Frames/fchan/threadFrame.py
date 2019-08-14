from Frames.abstractFrame import AbstractFrame
from Frames.builders.chanThreadBuilder import ChanThreadBuilder

class ThreadFrame(AbstractFrame, ChanThreadBuilder):
    def __init__(self, boardString, threadNumber, urwidViewManager, uFilter = None):
        super().__init__(urwidViewManager, uFilter)

        self.boardString = boardString
        self.threadNumber = threadNumber

        self.threadWidgetDict = {}

        self.url = 'https://a.4cdn.org' + self.boardString + 'thread/' + str(self.threadNumber) + '.json'
        # self.imageUrl = 'http://boards.4chan.org' + self.boardString + 'thread/' + str(self.threadNumber)
        self.imgPrefix = 'https://a.4cdn.org/'
        self.headers = {}

        self.postReplyDict = {}

        self.load()
        self.headerString = f'TerminusBrowser: {self.boardString} -- {str(self.threadNumber)}'

    # Overrides super
    def loader(self):
        self.comments = self.getJSONThread()
        self.contents = self.buildFrame()
