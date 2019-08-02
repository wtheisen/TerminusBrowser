# FocusMixin and CommandBar(Input) based on https://github.com/csrgxtu/Drogo/

import urwid, re, collections

from debug import DEBUG
from autocomplete import autoComplete


class QuotePreview(urwid.WidgetWrap):
    signals = ['close']
    def __init__(self, quoteNumber, urwidViewManager):
        currViewThreadWidgets = urwidViewManager.currFocusView.frame.postWidgetDict

        close_button = urwid.Button("Hide")
        urwid.connect_signal(close_button, 'click', lambda button:self._emit("close"))
        cleanQuoteNumber = re.sub("[^0-9]", "", str(quoteNumber))
        widgetList = currViewThreadWidgets[cleanQuoteNumber]
        widgetList.append(close_button)
        DEBUG(widgetList)
        fill = urwid.Filler(urwid.LineBox(urwid.Pile(widgetList)))
        self.__super.__init__(urwid.AttrWrap(fill, 'quotePreview'))

class QuoteButton(urwid.PopUpLauncher):
    def __init__(self, quoteNumber, urwidViewManager):
        self.quoteNumber = quoteNumber
        self.uvm = urwidViewManager

        self.__super.__init__(urwid.Button(str(quoteNumber)))
        urwid.connect_signal(self.original_widget, 'click', lambda button: self.open_pop_up())

    def create_pop_up(self):
        pop_up = QuotePreview(self.quoteNumber, self.uvm)
        urwid.connect_signal(pop_up, 'close', lambda button: self.close_pop_up())
        return pop_up

    def get_pop_up_parameters(self):
        return {'left':0, 'top':1, 'overlay_width':128, 'overlay_height':12}

class FocusMixin(object):
    def mouse_event(self, size, event, button, x, y, focus):
        if focus and hasattr(self, '_got_focus') and self._got_focus:
            self._got_focus()
        return super(FocusMixin,self).mouse_event(size, event, button, x, y, focus)

class CommandBar(FocusMixin, urwid.Edit):
    signals=['command_entered', 'exit_command']

    def __init__(self, gotFocus, urwidViewManager):
        urwid.Edit.__init__(self)
        self.historyList = collections.deque(maxlen=1000)
        self.historyIndex = -1
        self.gotFocus = gotFocus
        self.uvm = urwidViewManager

    def keypress(self, size, key):
        if key == 'esc':
            urwid.emit_signal(self, 'exit_command')

        if key == 'tab':
            autoComplete(self)

        if key == 'enter':
            command = self.edit_text.strip()
            if command:
                self.edit_text = u''
                self.historyList.append(command)
                urwid.emit_signal(self, 'command_entered', command)
            self.historyIndex = len(self.historyList)
            self.edit_text = u''

        if key == 'up':
            self.historyIndex -= 1

            if self.historyIndex < 0:
                self.historyIndex = 0
            else:
                self.edit_text = self.historyList[self.historyIndex]

        if key == 'down':
            self.historyIndex += 1

            if self.historyIndex >= len(self.historyList):
                self.historyIndex = len(self.historyList)
                self.edit_text = u''
            else:
                self.edit_text = self.historyList[self.historyIndex]
        else:
            urwid.Edit.keypress(self, size, key)

class HistoryMenu(urwid.WidgetWrap):
    """A dialog that appears with nothing but a close button """
    signals = ['close']
    def __init__(self, urwidViewManager):
        uvm = urwidViewManager
        close_button = urwid.Button("that's pretty cool")
        urwid.connect_signal(close_button, 'click',
            lambda button:self._emit("close"))

        historyButtonList = []
        for i in uvm.history:
            historyButtonList.append(urwid.Button(str(i), uvm.displayThread))

        pile = urwid.Pile(historyButtonList)
        # pile = urwid.Pile([urwid.Text(
        #     "^^  I'm attached to the widget that opened me. "
        #     "Try resizing the window!\n"), close_button])
        fill = urwid.Filler(pile)
        self.__super.__init__(urwid.AttrWrap(fill, 'popbg'))

class HistoryButton(urwid.PopUpLauncher):
    def __init__(self, urwidViewManager):
        self.uvm = urwidViewManager
        hButton = urwid.Button('History')
        hButton._label.align = 'right'
        self.__super.__init__(hButton)
        urwid.connect_signal(self.original_widget, 'click',
            lambda button: self.open_pop_up())

    def create_pop_up(self):
        pop_up = HistoryMenu(self.uvm)
        urwid.connect_signal(pop_up, 'close',
            lambda button: self.close_pop_up())
        return pop_up

    def get_pop_up_parameters(self):
        return {'left':0, 'top':1, 'overlay_width':32, 'overlay_height':7}
