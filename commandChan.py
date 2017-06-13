import sys, urwid, time

import requests, json, collections, re
from bs4 import BeautifulSoup

import urwid.raw_display
import urwid.web_display

################################################################################

class QuotePreview(urwid.WidgetWrap):
    """A dialog that appears with nothing but a close button """
    signals = ['close']
    def __init__(self, quoteNumber):
        global currentThreadWidgets
        close_button = urwid.Button("Hide")
        urwid.connect_signal(close_button, 'click', lambda button:self._emit("close"))
        cleanQuoteNumber = re.sub("[^0-9]", "", str(quoteNumber))
        fill = urwid.Filler(urwid.Pile([currentThreadWidgets[cleanQuoteNumber], close_button]))
        self.__super.__init__(urwid.AttrWrap(fill, 'quotePreview'))

class QuoteButton(urwid.PopUpLauncher):
    def __init__(self, quoteNumber):
        self.quoteNumber = quoteNumber
        self.__super.__init__(urwid.Button(str(quoteNumber)))
        urwid.connect_signal(self.original_widget, 'click', lambda button: self.open_pop_up())

    def create_pop_up(self):
        pop_up = QuotePreview(self.quoteNumber)
        urwid.connect_signal(pop_up, 'close', lambda button: self.close_pop_up())
        return pop_up

    def get_pop_up_parameters(self):
        global currentThreadWidgets
        return {'left':0, 'top':1, 'overlay_width':128, 'overlay_height':12}

######################### CATALOG PARSERS ######################################

def getJSONCatalog(url):
    response = requests.get(url)
    data = response.json()

    if "4cdn" in url:
        return parseFourCatalog(data)

def parseFourCatalog(data):
    titles = collections.OrderedDict()
    for i in range(0, 10):
        page = data[i]
        threadsList = page["threads"]
        for j in range(0, len(threadsList)):
            titles[threadsList[j]["semantic_url"]] = str(threadsList[j]["no"]) + '::' + str(threadsList[j]["replies"]) + '::' + str(threadsList[j]["images"])
    return titles

########################### THREAD PARSERS #####################################

def getJSONThread(url, chan, threadNumber):
    if "4chan" in chan:
        response = requests.get(url + str(threadNumber) + '.json')
        data = response.json()
        return parseFourThread(data)

def parseFourThread(data):
    comments = collections.OrderedDict()
    posts = data["posts"]
    for post in posts:
        try:
            imageBool = post['filename']
            try:
                comments[post["no"]] = post["com"] + '::' + 'image'
            except:
                comments[post["no"]] = '::image'
        except:
            try:
                comments[post["no"]] = post["com"]
            except:
                comments[post["no"]] = ''
    return comments

def getImageUrls(url, board):

    def load(url):
        req = requests.get(url)
        return str(req.content)

    thread_link = url
    page = BeautifulSoup(load(thread_link), "lxml")
    extensionList = ('.jpg', '.jpeg', '.png', '.gif', '.webm')
    images = []

    for img in page.find_all('a', href=True):
        if board in str(img) and 'i.4cdn.org' in str(img):
            tagList = str(img).split('"')
            for tag in tagList:
                if board in str(tag):
                    if any(extension in tag for extension in extensionList):
                        images.append(str(tag))

    return images

def commentTagParser(postNum, comment, imageURL=None):
    soup = BeautifulSoup(comment, "html.parser")
    tags = [str(tag) for tag in soup.find_all()]
    contents = []

    global currentThreadOPNumber

    test = re.split('<|>', comment)

    contents.append(urwid.Text(str(postNum).strip()))
    contents.append(urwid.Divider('-'))

    quote = False
    comment = False
    codeBlock = False
    inlineCode = []
    for item in test:
        item = item.encode('utf-8')
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

            if str(currentThreadOPNumber) == item[2:]:
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
        contents.append(urwid.Text('img: ' + str(imageURL)))
    else:
        contents.append(urwid.Text('img: '))

    return urwid.Pile(contents)

################################################################################

boards = ['/g/', '/v/', '/tv/', '/sp/', '/fa/', '/pol/', '/vg/',
          '/a/', '/b/', '/c/', '/d/', '/e/',
          '/f/', '/gif/', '/h/', '/hr/', '/k/',
          '/m/', '/o/', '/p/', '/r/', '/s/',
          '/t/', '/u/', '/vr/',
          '/w/', '/wg/', '/i/', '/ic/', '/r9k/',
          '/s4s/', '/vip/', '/cm/', '/hm/', '/lgbt/',
          '/y/', '/3/', '/aco/', '/adv/', '/an/',
          '/asp/', '/bant/', '/biz/', '/cgl/', '/ck/',
          '/co/', '/diy/', '/fit/', '/gd/', '/hc/',
          '/his/', '/int/', '/jp/', '/lit/', '/mlp/',
          '/mu/', '/n/', '/news/', '/out/', '/po/',
          '/qst/', '/sci/', '/soc/', '/tg/', 'toy',
          '/trv/', '/vp/', '/wsg/', '/wsr/', '/x/']

boardListWidget = None

currentBoard = ''
currentBoardWidget = None

currentThread = ''
currentThreadWidgets = None
currentThreadOPNumber = None

watchedThreads = []

level = 0

################################################################################

def main():

    header = urwid.AttrWrap(urwid.Text('CommandChan'), 'header')

    def threadWatcherWidget():
        global watchedThreads
        watcherWidget = urwid.Pile(watchedThreads)


    def getBoard(board):
        '''returns the board widget'''
        startTime = time.time()
        titles = getJSONCatalog('https://a.4cdn.org' + board + 'catalog.json')

        test = []

        for title, number in titles.items():
            title = title.replace('-', ' ')
            items = str(number).split('::')
            threadButton = urwid.Button(str(items[0]), displayThread)
            threadInfo = urwid.Text('Replies: ' + str(items[1]) + ' Images: ' + str(items[2]))
            threadList = [threadButton, urwid.Divider('-'), urwid.Divider(), urwid.Text(title), urwid.Divider(), urwid.Divider('-'), threadInfo]
            test.append(urwid.LineBox(urwid.Pile(threadList)))

        endTime = time.time()

        MEOW = urwid.GridFlow(test, 30, 2, 2, 'center')
        listbox_content = [MEOW]

        listbox = urwid.ListBox(urwid.SimpleListWalker(listbox_content))

        return listbox, (endTime - startTime), len(titles)

    def getThread(board, threadNum):
        startTime = time.time()
        comments = getJSONThread('https://a.4cdn.org' + board + 'thread/', '4chan', threadNum)

        global currentThreadWidgets

        test = []

        temp = {}

        def deDup(seq):
            seen = set()
            seen_add = seen.add
            return [x for x in seq if not (x in seen or seen_add(x))]

        images = getImageUrls('http://boards.4chan.org' + board + 'thread/' + str(threadNum), board)
        images = [ img for img in images if "s" not in img ]
        images = deDup(images)
        for i in range(0, len(images)):
            images[i] = 'http:' + images[i]

        for num, comment in comments.items():
            comment = comment.split('::')

            try:
                hasImage = comment[1]
                comment = comment[0]
                commentWidget = urwid.LineBox(commentTagParser(num, comment, images.pop(0)))
            except:
                if comment == 'image':
                    commentWidget = urwid.LineBox(commentTagParser(num, '', images.pop(0)))
                else:
                    comment = comment[0]
                    commentWidget = urwid.LineBox(commentTagParser(num, comment))

            test.append(commentWidget)
            temp[str(num).split()[0]] = commentWidget

        currentThreadWidgets = temp

        endTime = time.time()

        listbox_content = test
        listbox = urwid.ListBox(urwid.SimpleListWalker(listbox_content))

        return listbox, (endTime - startTime), len(comments)

    def displayBoard(button):
        global currentBoard
        currentBoard = button.get_label()
        global level
        level = 1

        temp, parseTime, itemCount = getBoard(button.get_label())

        global currentBoardWidget
        currentBoardWidget = urwid.LineBox(urwid.Pile([temp]))

        catalogue = urwid.Overlay(urwid.LineBox(urwid.Pile([temp])), test, 'center', ('relative', 90), 'middle', ('relative', 95))
        frame = urwid.Frame(urwid.AttrWrap(catalogue, 'body'), header=header)

        infoString = urwid.AttrWrap(urwid.Text('Board: ' + button.get_label()), 'header')
        timeString = urwid.AttrWrap(urwid.Text('Parsed ' + str(itemCount) + ' items in ' + str(parseTime)[0:6] + 's', 'right'), 'header')
        footerWidget = urwid.Columns([infoString, timeString])
        frame.footer = footerWidget

        urwid.MainLoop(frame, palette, screen, unhandled_input=unhandled, pop_ups=True).run()

    def displayThread(button):
        global currentThread
        currentThread = button.get_label()
        global level
        level = 2
        global currentBoardWidget
        global currentBoard

        listbox, parseTime, itemCount = getThread(currentBoard, currentThread)
        thread = urwid.Overlay(urwid.LineBox(urwid.Pile([listbox])), currentBoardWidget, 'center', ('relative', 60), 'middle', ('relative', 95))
        frame = urwid.Frame(urwid.AttrWrap(thread, 'body'), header=header)

        infoString = urwid.AttrWrap(urwid.Text('Board: ' + currentBoard + ', Thread: ' + button.get_label()), 'header')
        timeString = urwid.AttrWrap(urwid.Text('Parsed ' + str(itemCount) + ' items in ' + str(parseTime)[0:6] + 's', 'right'), 'header')
        footerWidget = urwid.Columns([infoString, timeString])

        frame.footer = footerWidget

        urwid.MainLoop(frame, palette, screen, unhandled_input=unhandled, pop_ups=True).run()

    boardButtons = []
    for board in boards:
        boardButtons.append(urwid.LineBox(urwid.AttrWrap(urwid.Button(board, displayBoard), 'center')))

    buttonGrid = urwid.GridFlow(boardButtons, 12, 2, 2, 'center')
    listbox_content = [buttonGrid]

    test = urwid.ListBox(urwid.SimpleListWalker(listbox_content))

    frame = urwid.Frame(urwid.AttrWrap(test, 'body'), header=header)

    global boardListWidget
    boardListWidget = frame

    def unhandled(key):
        if key == 's' and (level == 1 or level == 2):
            # add the currently focused thread to the thread watcher
            pass
        elif key == 'q' and level == 0:
            sys.exit()
        elif key =='q' and level == 1:
            global level
            level = 0
            global currentBoard
            currentBoard = ''
            global currentBoardWidget
            currentBoardWidget = None

            global boardListWidget
            urwid.MainLoop(boardListWidget, palette, screen, unhandled_input=unhandled).run()
        elif key == 'q' and level == 2:
            global level
            level = 1
            global currentBoard
            global currentBoardWidget

            catalogue = urwid.Overlay(currentBoardWidget, test, 'center', ('relative', 90), 'middle', ('relative', 95))
            frame = urwid.Frame(urwid.AttrWrap(catalogue, 'body'), header=header)
            frame.footer = urwid.AttrWrap(urwid.Text('Board: ' + currentBoard), 'header')

            urwid.MainLoop(frame, palette, screen, unhandled_input=unhandled).run()


    palette = [
        ('body', 'light gray', 'black', 'standout'),
        ('quote', 'light cyan', 'black'),
        ('greenText', 'dark green', 'black'),
        ('reverse', 'light gray', 'black'),
        ('header', 'white', 'dark red', 'bold'),
        ('important', 'dark blue', 'light gray', ('standout', 'underline')),
        ('editfc', 'white', 'dark blue', 'bold'),
        ('editbx', 'light gray', 'dark blue'),
        ('editcp', 'black', 'light gray', 'standout'),
        ('bright', 'dark gray', 'light gray', ('bold', 'standout')),
        ('buttn', 'black', 'dark cyan'),
        ('buttnf', 'white', 'dark blue', 'bold'),
        ('quotePreview', 'light gray', 'black')
        ]

    # use appropriate Screen class
    if urwid.web_display.is_web_request():
        screen = urwid.web_display.Screen()
    else:
        screen = urwid.raw_display.Screen()


    urwid.MainLoop(frame, palette, screen, unhandled_input=unhandled, pop_ups=True).run()

def setup():
    urwid.web_display.set_preferences("Urwid Tour")
    # try to handle short web requests quickly
    if urwid.web_display.handle_short_request():
        return

    main()

if '__main__'==__name__ or urwid.web_display.is_web_request():
    setup()
