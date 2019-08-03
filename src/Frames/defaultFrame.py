import urwid, pyfiglet, requests

from debug import DEBUG

class DefaultFrame(urwid.WidgetWrap):
    def __init__(self, welcome=False):
        self.headerString = 'CommandChan'
        self.footerStringRight = f''
        self.url = 'Welcome Screen'

        if welcome:
            r = requests.get('https://api.github.com/repos/wtheisen/commandChan/commits')
            data = r.json()

            welcomeText = pyfiglet.figlet_format('commandChan') + '\nRecent Commits:\n'
            
            count = 0
            for cData in data:
                commit = cData['commit']
                welcomeText += f'\n {commit["author"]["name"]}: {commit["message"]}'

                if count < 4:
                    count += 1
                else:
                    break

            self.contents = urwid.Text(welcomeText, 'center')
        else:
            self.contents = urwid.Text('')

        self.contents = urwid.Filler(self.contents)
        urwid.WidgetWrap.__init__(self, self.contents)
