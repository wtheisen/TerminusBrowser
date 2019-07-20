commandList = [
                'search',
                'thread',
                'stickies',
                'board',
                'post',
                'reply',
                'threadStyle',
                'boardStyle',
                'reddit',
                '4chan'
            ]

def autoComplete(editBox):
    currText = editBox.get_edit_text()
    try:
        inputList = currText.split()[0]
    except IndexError:
        return

    if len(inputList) == 1: #completing first bit
        currCommand = currText.split()[0]
        matches = [x for x in commandList if x.startswith(currCommand)]
        shortestMatch = min(matches, key=len)
        editBox.set_edit_text(shortestMatch)
        editBox.set_edit_pos(len(shortestMatch))
    elif len(inputList) == 2: #completing argument
        pass
