import urwid, re, time, collections, requests

class BoardFrame(urwid.WidgetWrap):
    def __init__(self, boardString, urwidViewManager, uFilter=None):
        self.uvm = urwidViewManager
        self.boardString = boardString
        self.uFilter = uFilter

        self.url = 'https://a.4cdn.org' + self.boardString + 'catalog.json'
        self.threadNums = []
        self.info_text = 'Replies: {} Images: {}'
        self.parsedItems = 0

        self.startTime = time.time()

        self.titles = self.getJSONCatalog(self.url)
        self.contents = urwid.Pile(self.buildFrame(boardString))
        urwid.WidgetWrap.__init__(self, self.contents)
        self.endTime = time.time()
        self.footerStringRight = f'Parsed {self.parsedItems} items in {(self.endTime - self.startTime):.4f}s'

    def buildFrame(self, board):
        '''returns the board widget'''

        threadButtonList = []

        for title, threadInfo in self.titles.items():
            title = title.replace('-', ' ')
            if self.uFilter:
                if re.search(self.uFilter.lower(), title.lower()):
                    threadButton = urwid.Button(str(threadInfo[0]), self.changeFrameThread)
                    threadInfo = urwid.Text(self.info_text.format(str(threadInfo[1]),str(threadInfo[2])))
                    threadList = [threadButton, urwid.Divider('-'), urwid.Divider(), urwid.Text(title), urwid.Divider(), urwid.Divider('-'), threadInfo]
                    threadButtonList.append(urwid.LineBox(urwid.Pile(threadList)))
            else:
                threadButton = urwid.Button(str(threadInfo[0]), self.changeFrameThread)
                threadInfo = urwid.Text(self.info_text.format(str(threadInfo[1]), str(threadInfo[2])))
                threadList = [threadButton, urwid.Divider('-'), urwid.Divider(), urwid.Text(title), urwid.Divider(), urwid.Divider('-'), threadInfo]
                threadButtonList.append(urwid.LineBox(urwid.Pile(threadList)))

        self.parsedItems = len(threadButtonList)
        catalogueButtons = urwid.GridFlow(threadButtonList, 30, 2, 2, 'center')
        listbox = urwid.ListBox(urwid.SimpleListWalker([catalogueButtons]))

        self.uvm.itemCount = len(threadButtonList)
        return [listbox]

    def getJSONCatalog(self, url):
        response = requests.get(url, headers={})
        data = response.json()

        return self.parseFourCatalog(data)

    def parseFourCatalog(self, data):
        titles = collections.OrderedDict()
        for i in range(0, 10):
            page = data[i]
            threadsList = page["threads"]
            for j in range(0, len(threadsList)):
                titles[threadsList[j]["semantic_url"]] = (threadsList[j]["no"], threadsList[j]["replies"], threadsList[j]["images"])
                self.threadNums.append(threadsList[j]["no"])
        return titles

    def changeFrameThread(self, button):
        import commands
        commands.thread(self.uvm, self.boardString, button.get_label())