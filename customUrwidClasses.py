import urwid, re, collections

from commandHandlerClass import CommandHandler
from debug import DEBUG

class QuotePreview(urwid.WidgetWrap):
    signals = ['close']
    def __init__(self, quoteNumber):
        global currentThreadWidgets
        close_button = urwid.Button("Hide")
        urwid.connect_signal(close_button, 'click', lambda button:self._emit("close"))
        cleanQuoteNumber = re.sub("[^0-9]", "", str(quoteNumber))
        fill = urwid.Filler(urwid.LineBox(urwid.Pile([currentThreadWidgets[cleanQuoteNumber], close_button])))
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
        return {'left':0, 'top':1, 'overlay_width':128, 'overlay_height':12}

class FocusMixin(object):
    def mouse_event(self, size, event, button, x, y, focus):
        if focus and hasattr(self, '_got_focus') and self._got_focus:
            self._got_focus()
        return super(FocusMixin,self).mouse_event(size, event, button, x, y, focus)

class CommandBar(FocusMixin, urwid.Edit):
# class CommandBar(urwid.Edit):
    signals=['command_entered', 'exit_insert']

    def __init__(self, got_focus=None):
        urwid.Edit.__init__(self)
        self.history=collections.deque(maxlen=1000)
        self._history_index=-1
        self._got_focus=got_focus

    def keypress(self, size, key):
        if key == 'esc':
            urwid.emit_signal(self, 'exit_insert')
        if key == 'enter':
            line=self.edit_text.strip()
            if line:
                self.edit_text=u''
                self.history.append(line)
                urwid.emit_signal(self, 'command_entered', line)
            self._history_index=len(self.history)
            self.edit_text=u''
        if key=='up':
            self._history_index-=1
            if self._history_index< 0:
                self._history_index= 0
            else:
                self.edit_text=self.history[self._history_index]
        if key=='down':
            self._history_index+=1
            if self._history_index>=len(self.history):
                self._history_index=len(self.history)
                self.edit_text=u''
            else:
                self.edit_text=self.history[self._history_index]
        else:
            urwid.Edit.keypress(self, size, key)