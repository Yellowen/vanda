# -----------------------------------------------------------------------------
#    Ultra Blog - Data type base blog application for Vanda platform
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

import logging


class BaseType(object):

    form = None
    name = None

    def get_form(self):
        return self.form


class PostType(object):

    _registery = dict()

    def __init__(self):
        #self.debug
        self.logger = logging.getLogger()

    def register(self, type_class):
        """
        Register types class of an Vanda applications into Ultra Blog.
        """

        if not issubclass(type_class, BaseType):
            raise TypeError("'%s' must be a BaseType subclass." %
                            type_class)

        # Checking the provided base_class application property.
        try:
            type_name = getattr(type_class,
                                       "name").lower()
        except AttributeError:
            raise AttributeError("'%s' did not have 'type_name'." %
                                 type_class + ' property')

        if type_name in self._registery.keys():
            self.logger.warning("'%s' already registered." % type_name)
        else:
            self._registery[type_name] = type_class()


    def admin_view(self, req):
        """
        
        """
        pass


post_types = PostType()
