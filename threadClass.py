#Thread Class
import requests, json, collections
import threadViewClasses

from bs4 import BeautifulSoup

def displayThread():
    pass

class Thread:
    def __init__(self, board, number):
        self.board = board
        self.number = str(number)
        self.url = 'https://a.4cdn.org' + self.board + 'thread/' + self.number

        self.comments = self.getJSONThread(self.url)
        self.images   = self.getImageUrls(self.url, self.board)


    def getJSONThread(self, url):
        response = requests.get(url + '.json')
        data = response.json()
        return parseFourThread(data)

    def parseFourThread(data):
        comments = collections.OrderedDict()
        posts = data["posts"]
        global currentThreadOPNumber

        replies = {}
        for post in posts:
            if str(post["resto"]) == '0':
                currentThreadOPNumber = str(post["no"])

            replies[str(post["no"])] = []
            try:
                comStr = BeautifulSoup(post["com"], 'lxml')
                quotes = comStr.find('a')
                quotes = quotes.attrs['href']
                replies += quotes
            except:
                pass

            try:
                imageBool = post['filename']
                try:
                    comments[str(post["no"]) + ' ' + post["now"]] = post["com"] + '::image'
                except:
                    comments[str(post["no"]) + ' ' + post["now"]] = '::image'
            except:
                try:
                    comments[str(post["no"]) + ' ' + post["now"]] = post["com"]
                except:
                    comments[str(post["no"]) + ' ' + post["now"]] = ''
        return comments

    def getImageUrls(url, board):
        def load(url):
            req = requests.get(url)
            return str(req.content)

        thread_link = url
        page = BeautifulSoup(load(thread_link), "lxml")
        extensionList = ('.jpg', '.jpeg', '.png', '.gif', '.webm')
        images = []

        print('meow')

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
            with open('log.txt', 'a+') as out:
                out.write(item + '\n')

            # item = item.encode('utf-8', 'xmlcharrefreplace').decode()
            # item = bytes(item, "utf-8").decode()
            # item = item.encode('utf-8')
            # item = ascii(item)
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
                item = item.replace('\r', '\n')

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
            contents.append(urwid.Text('Image: ' + str(imageURL)))
        else:
            contents.append(urwid.Text('Image: '))

        contents.append(urwid.Text('Replies: '))

        return urwid.Pile(contents)
