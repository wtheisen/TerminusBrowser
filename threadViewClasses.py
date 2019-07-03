#Thread view classes

class urwidThreadView:
    def getThread(board, threadNum, images, comments):
        startTime = time.time()
        test = []
        temp = {}

        def deDup(seq):
            seen = set()
            seen_add = seen.add
            return [x for x in seq if not (x in seen or seen_add(x))]

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

    def displayThread(button, thread=None):
        global currentThread
        if thread:
            currentThread = thread
        else:
            currentThread = button.get_label()
        global level
        level = 2
        global currentBoardWidget
        global currentBoard

        listbox, parseTime, itemCount = getThread(currentBoard, currentThread)
        thread = urwid.Overlay(urwid.LineBox(urwid.Pile([listbox])), currentBoardWidget, 'center', ('relative', 60), 'middle', ('relative', 95))
        frame = urwid.Frame(urwid.AttrWrap(thread, 'body'), header=header)

        infoString = urwid.AttrWrap(urwid.Text('Mode: ' + str(currentMode) + ', Board: ' + currentBoard + ', Thread: ' + currentThread), 'header')
        timeString = urwid.AttrWrap(urwid.Text('Parsed ' + str(itemCount) + ' items in ' + str(parseTime)[0:6] + 's', 'right'), 'header')
        footerWidget = urwid.Columns([infoString, timeString])

        frame.footer = footerWidget

        urwid.MainLoop(frame, palette, screen, unhandled_input=unhandled, pop_ups=True).run()
