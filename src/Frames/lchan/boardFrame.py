from Frames.abstractFrame import AbstractFrame
from Frames.builders.chanBoardBuilder import ChanBoardBuilder

class BoardFrame(AbstractFrame, ChanBoardBuilder):
    def __init__(self, boardString, urwidViewManager, uFilter=None):
        super().__init__(urwidViewManager, uFilter)
        self.boardString = boardString

        self.url = 'https://www.lainchan.org' + self.boardString + 'catalog.json'
        self.threadNums = []
        self.info_text = 'Replies: {} Images: {}'

        self.load()
        self.headerString = f'TerminusBrowser - lainchan: {self.boardString}'

    # Overrides super
    def loader(self):
        self.threadsDict = self.getJSONCatalog(self.url)
        self.contents = self.buildFrame(self.boardString)
