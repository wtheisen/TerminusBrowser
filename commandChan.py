import parsers
import sys, urwid
import urwid.raw_display
import urwid.web_display

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
level = 0

def main():

    header = urwid.AttrWrap(urwid.Text('CommandChan'), 'header')

    def getBoard(board):
        '''returns the board widget'''
        titles = parsers.getJSONCatalog('https://a.4cdn.org' + board + 'catalog.json')

        test = []

        for title, number in titles.items():
            title = title.replace('-', ' ')
            items = str(number).split('::')
            threadButton = urwid.Button(str(items[0]), displayThread)
            threadInfo = urwid.Text('Replies: ' + str(items[1]) + ' Images: ' + str(items[2]))
            threadList = [threadButton, urwid.Divider('-'), urwid.Divider(), urwid.Text(title), urwid.Divider(), urwid.Divider('-'), threadInfo]
            test.append(urwid.LineBox(urwid.Pile(threadList)))

        MEOW = urwid.GridFlow(test, 30, 2, 2, 'center')
        listbox_content = [MEOW]

        listbox = urwid.ListBox(urwid.SimpleListWalker(listbox_content))

        return listbox

    def getThread(board, threadNum):
        comments = parsers.getJSONThread('https://a.4cdn.org' + board + 'thread/', '4chan', threadNum)

        test = []

        for num, comment in comments.items():
            test.append(urwid.LineBox(parsers.commentTagParser(num, comment)))

        listbox_content = test

        listbox = urwid.ListBox(urwid.SimpleListWalker(listbox_content))

        return listbox

    def displayBoard(button):
        global currentBoard 
        currentBoard = button.get_label()
        global level
        level = 1

        temp = getBoard(button.get_label())

        global currentBoardWidget
        currentBoardWidget = temp

        catalogue = urwid.Overlay(temp, test, 'center', ('relative', 90), 'middle', ('relative', 95))
        frame = urwid.Frame(urwid.AttrWrap(catalogue, 'body'), header=header)
        frame.footer = urwid.AttrWrap(urwid.Text('Board: ' + button.get_label()), 'header')

        urwid.MainLoop(frame, palette, screen, unhandled_input=unhandled).run()

    def displayThread(button):
        global currentThread 
        currentThread = button.get_label()
        global level
        level = 2
        global currentBoardWidget
        global currentBoard

        listbox = getThread(currentBoard, currentThread)
        thread = urwid.Overlay(listbox, currentBoardWidget, 'center', ('relative', 60), 'middle', ('relative', 95))
        frame = urwid.Frame(urwid.AttrWrap(thread, 'body'), header=header)
        frame.footer = urwid.AttrWrap(urwid.Text('Board: ' + currentBoard + ', Thread: ' + button.get_label()), 'header')

        urwid.MainLoop(frame, palette, screen, unhandled_input=unhandled).run()

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
        if key == 'q' and level == 0:
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
        ]


    # use appropriate Screen class
    if urwid.web_display.is_web_request():
        screen = urwid.web_display.Screen()
    else:
        screen = urwid.raw_display.Screen()


    urwid.MainLoop(frame, palette, screen, unhandled_input=unhandled).run()

def setup():
    urwid.web_display.set_preferences("Urwid Tour")
    # try to handle short web requests quickly
    if urwid.web_display.handle_short_request():
        return

    main()

if '__main__'==__name__ or urwid.web_display.is_web_request():
    setup()
