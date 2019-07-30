import urwid, pyfiglet

class DefaultFrame(urwid.WidgetWrap):
    def __init__(self, welcome=False):
        self.headerString = 'CommandChan'
        self.footerStringRight = f''

        if welcome:
            self.contents = urwid.Button(pyfiglet.figlet_format('commandChan'), 'center')
        else:
            self.contents = urwid.Button('')

        self.contents = urwid.Filler(self.contents)
        urwid.WidgetWrap.__init__(self, self.contents)
