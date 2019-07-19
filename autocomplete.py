from debug import DEBUG
commandList = [
                'search',
                'thread',
                'stickies',
                'history',
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
        inputList = currText.split()
    except IndexError:
        return

    if len(inputList) == 1: #completing first bit
        currCommand = currText.split()[0]
        matches = [x for x in commandList if x.startswith(currCommand)]
        # Check to toggle for previous match
        if len(matches) == 1:
            currCommand = currCommand[:3]
            matches = [x for x in commandList if x.startswith(currCommand)]
        match = min(matches, key=len)
        if currCommand in commandList:
            try:
                match = matches[1]
            except IndexError:
                pass
        editBox.set_edit_text(match)
        editBox.set_edit_pos(len(match))