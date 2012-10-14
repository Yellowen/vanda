# -----------------------------------------------------------------------------
#    Debbox - Modern administration panel for Debian GNU/Linux
#    Copyright (C) 2011 Some Hackers In Town
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# -----------------------------------------------------------------------------

from debbox.core.logging import logger


class SectionNode(object):
    """
    Dashboard menu section base class
    """
    permissions = []
    title = None
    name = None
    weight = 300

    def __init__(self):
        self._item_registry = {}
        self.logger = logger

    def items_name_list(self):
        return self._item_registry.keys()

    def get_items(self, user):
        """
        Return a list from section items like:
            [(weight, title, link), . . .]
        """
        items_list = list()
        append = items_list.append

        # get the list representation of each item object
        for item in self._item_registry:
            tmp = self._item_registry[item].get_as_list(user)
            if tmp:
                append(tmp)

        items_list.sort()
        return items_list
            
    def register_item(self, item_node):
        """
        Registering a item_node.
        """
        # item_class should be direct or indirect instance of ItemNode
        # class
        if not issubclass(item_node, ItemNode):
            raise TypeError("'%s' shoud be a subclass of ItemNode" %
                            item_node.__name__)
        # Checking the section name.
        try:
            # each itemNode subclass should have a name property
            item_name = getattr(item_node, "name")
        except AttributeError:
            raise AttributeError("'%s' node does not have a " %
                                 item_node.__name__ +
                                 "'name' property")
        if not item_name:
            raise AttributeError("'%s' node does not have a " %
                                 item_node.__name__ +
                                 "'name' property")
        if item_name in self._item_registry.keys():
            # TODO: Can new item class override the exists one?
            self.logger.debug("An Item with the '%s' name already registered.")
            return False

        # registring item_node
        self._item_registry[item_name.lower()] = item_node()
        return True


class ItemNode(object):
    """
    Dashboard menu item base class
    """
    permissions = []
    title = None
    link = None
    parent = None
    weight = 500
    name = None

    def __init__(self):
        self.logger = logger

    def get_as_list(self, user):
        """
        return a list of ItemNode properties.
        """
        # TODO: check the user authentication here
        return [self.weight, self.title, self.link]

    def is_enable(self):
        """
        Does link is enable?
        """
        return True
