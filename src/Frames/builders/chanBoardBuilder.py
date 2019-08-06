import urwid, re, time, collections, requests

from debug import DEBUG

class ChanBoardBuilder():

    def buildFrame(self, board):
        '''returns the board widget'''

        threadButtonList = []

        for threadNumber, threadInfo in self.threadsDict.items():
            title = str(threadInfo[0]).replace('-', ' ')
            if self.uFilter:
                if re.search(self.uFilter.lower(), title.lower()):
                    threadButton = urwid.Button(str(threadNumber), self.changeFrameThread)
                    threadInfo = urwid.Text(self.info_text.format(str(threadInfo[1]),str(threadInfo[2])))
                    threadList = [threadButton, urwid.Divider('-'), urwid.Divider(), urwid.Text(title), urwid.Divider(), urwid.Divider('-'), threadInfo]
                    threadButtonList.append(urwid.LineBox(urwid.Pile(threadList)))
            else:
                threadButton = urwid.Button(str(threadNumber), self.changeFrameThread)
                threadInfo = urwid.Text(self.info_text.format(str(threadInfo[1]), str(threadInfo[2])))
                threadList = [threadButton, urwid.Divider('-'), urwid.Divider(), urwid.Text(title), urwid.Divider(), urwid.Divider('-'), threadInfo]
                threadButtonList.append(urwid.LineBox(urwid.Pile(threadList)))

        self.parsedItems = len(threadButtonList)
        catalogueButtons = urwid.GridFlow(threadButtonList, 30, 2, 2, 'center')
        listbox = urwid.ListBox(urwid.SimpleListWalker([catalogueButtons]))

        self.uvm.itemCount = len(threadButtonList)
        return urwid.Pile([listbox])

    def getJSONCatalog(self, url):
        response = requests.get(url, headers={})
        data = response.json()

        return self.parseFourCatalog(data)

    def parseFourCatalog(self, data):
        threadsDict = collections.OrderedDict()
        # for i in range(0, 10):
        # DEBUG(data)
        for page in data:
            for k, v in page.items():
                DEBUG(k)
                if k == "threads":
                    threadsList = v
                    DEBUG(len(threadsList))
                    for thread in threadsList:
                        threadsDict[thread["no"]] = (thread["semantic_url"] if "semantic_url" in thread else thread["sub"] if "sub" in thread else "",
                                                    thread["replies"], thread["images"])
        return threadsDict

    def changeFrameThread(self, button):
        from commandHandlerClass import CommandHandler
        ch = CommandHandler(self.uvm)
        ch.routeCommand('thread ' + self.boardString + ' ' + button.get_label())
