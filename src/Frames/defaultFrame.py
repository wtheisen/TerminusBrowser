import urwid, pyfiglet

class DefaultFrame(urwid.WidgetWrap):
    def __init__(self, welcome=False):
        self.headerString = 'CommandChan'
        self.footerStringRight = f''
        self.url = 'Welcome Screen'

        if welcome:
            self.contents = urwid.Text(pyfiglet.figlet_format('commandChan'), 'center')
        else:
            self.contents = urwid.Text('')

        self.contents = urwid.Filler(self.contents)
        urwid.WidgetWrap.__init__(self, self.contents)
