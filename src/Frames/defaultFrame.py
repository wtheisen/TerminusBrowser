import urwid, pyfiglet, requests

from debug import DEBUG

class DefaultFrame(urwid.WidgetWrap):
    def __init__(self, welcome=False, test=False):
        self.headerString = 'TerminusBrowser'
        self.footerStringRight = f''
        self.url = 'Welcome Screen'

        if welcome:
            welcomeText = pyfiglet.figlet_format('TerminusBrowser') + '\nRecent Commits:\n'

            if not test:
                r = requests.get('https://api.github.com/repos/wtheisen/TerminusBrowser/commits')
                data = r.json()

                count = 0
                for cData in data:
                    commit = cData['commit']
                    cleanMessage = commit['message'].replace('\r', '').replace('\n\n', '\n')
                    welcomeText += f'\n {commit["author"]["name"]}: {cleanMessage}'

                    if count < 4:
                        count += 1
                    else:
                        break

            self.contents = urwid.Text(welcomeText, 'center')
        else:
            self.contents = urwid.Text('')

        self.contents = urwid.Filler(self.contents)
        urwid.WidgetWrap.__init__(self, self.contents)

def FrameFactory(frameClass):
    return lambda x: frameClass(*x)
