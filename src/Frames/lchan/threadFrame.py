from Frames.abstractFrame import AbstractFrame
from Frames.builders.chanThreadBuilder import ChanThreadBuilder

class ThreadFrame(AbstractFrame, ChanThreadBuilder):
    def __init__(self, boardString, threadNumber, urwidViewManager, uFilter = None):
        super().__init__(urwidViewManager, uFilter)

        self.boardString = boardString
        self.threadNumber = threadNumber

        self.threadWidgetDict = {}

        self.url = 'https://www.lainchan.org' + self.boardString + 'res/' + str(self.threadNumber) + '.json'
        self.imgPrefix = 'https://www.YEET.com/'

        self.headers = {}

        self.postReplyDict = {}

        self.load()
        self.headerString = f'TerminusBrowser - lainchan: {self.boardString} -- {str(self.threadNumber)}'

    # Overrides super
    def loader(self):
        self.comments = self.getJSONThread()
        self.contents = self.buildFrame()
