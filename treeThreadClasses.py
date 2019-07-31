import urwid
   
class CommentWidget(urwid.TreeWidget):
    unexpanded_icon = urwid.AttrMap(urwid.TreeWidget.unexpanded_icon,
        'dirmark')
    expanded_icon = urwid.AttrMap(urwid.TreeWidget.expanded_icon,
        'dirmark')

    def __init__(self, node):
        self._innerwidget = None
        self.info_text = 'score: {} user: {}'

        self.__super.__init__(node)
        
        self._has_child = self.get_node().get_value().replies != []
        self.expanded = (self.get_node().get_depth() < 3 or
                         not self._has_child)
        self.update_expanded_icon()

    def get_inner_widget(self):
        if self._innerwidget is None:
            self._innerwidget = self.load_inner_widget()
        return self._innerwidget

    def load_inner_widget(self):
        content = [urwid.Text(self.get_display_text()), urwid.Divider('-'),
                   urwid.Text(self.get_info_text())]
        return urwid.LineBox(urwid.Pile(content))

    def keypress(self, size, key):
        """allow subclasses to intercept keystrokes"""
        if key == 'right' and self._has_child:
            self.expanded = not self.expanded
            self.update_expanded_icon()
        else:
            key = self.__super.keypress(size, key)
        return key

    def get_display_text(self):
        return self.get_node().get_value().content

    def get_info_text(self):
        return self.info_text.format(self.get_node().get_value().score,
                                     self.get_node().get_value().userIden)


class CommentNode(urwid.ParentNode):
    """ Data storage object for interior/parent nodes """
    def load_widget(self):
        return CommentWidget(self)

    def load_child_keys(self):
        data = self.get_value()
        return range(len(data.replies))

    def load_child_node(self, key):
        """Return either an ExampleNode or ExampleParentNode"""
        childdata = self.get_value().replies[key]
        childdepth = self.get_depth() + 1
        childclass = CommentNode
        return childclass(childdata, parent=self, key=key, depth=childdepth)
