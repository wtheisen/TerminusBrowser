from Commands.SystemCommands import SystemCommandList
from Commands.ChanCommands import ChanCommandList
from Commands.RedditCommands import RedditCommandList
from debug import DEBUG


def autoComplete(editBox):
    currText = editBox.get_edit_text()
    try:
        inputList = currText.split()
    except IndexError:
        return

    commandList = (SystemCommandList + ChanCommandList + RedditCommandList)

    if len(inputList) == 1: #completing first bit
        currCommand = currText.split()[0]
        matches = [x for x in commandList if x.startswith(currCommand)]
        # Check to toggle for previous match
        if not len(matches):
            return
        elif len(matches) == 1:
            currCommand = currCommand[:2]
            matches = [x for x in commandList if x.startswith(currCommand)]
        match = min(matches, key=len)
        if currCommand in commandList:
            try:
                match = matches[1]
            except IndexError:
                pass
        editBox.set_edit_text(match)
        editBox.set_edit_pos(len(match))
    elif len(inputList) == 2:
        pass
