import requests, json, collections, urwid, re
from bs4 import BeautifulSoup

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
            comments[str(post["no"]) + '   ' + post["now"]] = post["com"]
        except:
            comments[str(post["no"]) + '   ' + post["now"]] = ''
    return comments

def commentTagParser(postNum, comment):
    soup = BeautifulSoup(comment, "html.parser")
    tags = [str(tag) for tag in soup.find_all()]
    contents = []

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

            contents.append(urwid.AttrWrap(urwid.Text(item), 'quote'))
            quote = False
        elif 'span class="quote' in item:
            comment = True
            continue
        elif comment:
            item = item.replace('&#039;', "'")
            item = item.replace('&quot;', '"')
            item = item.replace('&amp;', '&')
            item = item.replace('&gt;', '>')

            contents.append(urwid.AttrWrap(urwid.Text(item), 'greenText'))
            comment = False
        elif 'pre class="prettyprint"' in item:
            codeBlock = True
        else:
            item = item.replace('&#039;', "'")
            item = item.replace('&quot;', '"')
            item = item.replace('&amp;', '&')

            if not codeBlock:
                contents.append(urwid.Text(item))
            else:
                inlineCode.append(urwid.Text(item))

    contents.append(urwid.Divider())
    contents.append(urwid.Divider('-'))
    contents.append(urwid.Text('img: '))

    return urwid.Pile(contents)