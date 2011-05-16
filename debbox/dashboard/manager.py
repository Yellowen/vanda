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

from base import SectionNode, ItemNode


class DashboardManager(object):
    """
    Dashboard manager class. this class allow to application to register their
    own dashboard configuration class and control their dashboard property.
    """

    def __init__(self):
        self._menu_registry = {}
        self.logger = logger

    def menu_section(self, section_class):
        """
        Register a SectionNode subclass into dashboard menu.
        each application can add some section to dashboard menu but if
        a section exists int registry then old one used and new one will
        skip.
        """
        # section class shoud be a direct or indirect subclass of SectionNode
        # class
        if not issubclass(section_class, SectionNode):
            raise TypeError("'%s' shoud be a subclass of SectionNode" %
                            section_class.__class__)
        # Checking the section name.
        try:
            # each SectionNode subclass should have a name property
            section_name = section_class.__getattr__("name")
        except AttributeError:
            raise AttributeError("'%s' Section node does not have a " %
                                 section_class.__class__ +
                                 "'name' property")

        # does section_class already registered?
        if section_name in self._menu_registry.keys():
            # TODO: Can new section class override the exists one?
            self.logger.debug("A section with '%s' name already registered.")
            return

        # registring section_class into dashboard
        self._menu_registry[section_name] = section_class()

    def menu_item(self, item_class):
        """
        Register a ItemNode subclass into dashboard menu.
        each application can add some item to any dashboard menu section
        but if an item exists int registry then new one will apear with
        a new name.
        """
        # item_class should be direct or indirect instance of ItemNode
        # class
        if not issubclass(item_class, ItemNode):
            raise TypeError("'%s' shoud be a subclass of ItemNode" %
                            item_class.__class__)
        # Checking the section name.
        try:
            # each itemNode subclass should have a name property
            item_name = item_class.__getattr__("name")
        except AttributeError:
            raise AttributeError("'%s' node does not have a " %
                                 item_class.__class__ +
                                 "'name' property")
        # checking for item parent
        try:
            item_parent = item_class.__getattr__("parent")
        except AttributeError:
            raise AttributeError("'%s' node does not have a " %
                                 item_class.__class__ +
                                 "'parent' property")

        if not item_parent in self._menu_registry:
            # if parent section does not registered
            raise self.InvalidSection("'%s' section does not registered")
        # registering item into parent section via parent section code
        parent_section =  self._menu_registry[item_parent]
        parent_section.register_item(item_class):


dashboard = DashboardManager()
