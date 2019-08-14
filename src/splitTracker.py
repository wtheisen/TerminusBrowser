import urwid

from Views.viewClass import View

import logging
log = logging.getLogger(__name__)

class Column():
    def __init__(self):
        self.widgets = []

class Row():
    def __init__(self):
        self.widgets = []

def buildUrwidFromSplits(splitList):
    log.debug(type(splitList) is View)

    if type(splitList) is Column: 
        return urwid.Columns([buildUrwidFromSplits(x) for x in splitList.widgets])
    elif type(splitList) is Row:
        return urwid.Pile([buildUrwidFromSplits(x) for x in splitList.widgets])
    elif type(splitList) is View:
        return urwid.WidgetWrap(urwid.LineBox(splitList.frame))
