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
# -----------------------------------------------------------------------------
import logging
from django import forms


class PostType(object):
    """
    This class act as the basic class of all types that an application provids.
    """
    name = None

    # Admin form should be a model form
    # that collect data in admin interface
    admin_form = None
    verbose_name = None

    admin_class = None

    def __unicode__(self):
        return self.verbose_name


class BlogPostTypes(object):
    """
    This class handled the post registerd by other applications.
    """
    _registery = dict()

    def __init__(self):
        self.logger = logging.getLogger()

    def register(self, type_class):
        """
        Register types class of an Vanda applications into Ultra Blog.
        """

        if not issubclass(type_class, PostType):
            raise TypeError("'%s' must be a PostType subclass." %
                            type_class)

        # Checking the provided base_class application property.
        try:
            type_name = getattr(type_class,
                                       "name").lower()
        except AttributeError:
            raise AttributeError("'%s' did not have 'name'." %
                                 type_class + ' property')

        if type_name in self._registery.keys():
            self.logger.warning("'%s' already registered." % type_name)
        else:
            self._registery[type_name] = type_class()

    def get_form(self, type_name):
        """
        Return the form of type_name
        """
        if type_name.lower() in self._registery:
            return self._registery[type_name.lower()].admin_form
        else:
            return None

    def get_type(self, type_name):
        """
        Return the type class of type_name
        """
        return self._registery[type_name.lower()]

    def get_all_admin_forms(self):
        forms = []

        admin_forms = map(lambda x: [x, self._registery[x]],
                          self._registery.keys())

        return admin_forms


post_types = BlogPostTypes()
