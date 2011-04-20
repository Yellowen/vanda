# -----------------------------------------------------------------------------
#    VPKG - Vanda Package manager
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


class VPKGRouter(object):
    """
    A router to control all database operations on models in
    the VPKG application
    """

    def db_for_read(self, model, **hints):
        """
        Point all operations on vpkg models to 'vpkg'
        """
        if model._meta.app_label == 'vpkg':
            return 'vpkg'
        return None

    def db_for_write(self, model, **hints):
        """
        Point all operations on vpkg models to 'vpkg'
        """
        if model._meta.app_label == 'vpkg':
            return 'vpkg'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow any relation if a model in vpkg is involved
        """
        if obj1._meta.app_label == 'vpkg' or \
               obj2._meta.app_label == 'vpkg':
            return True
        return None

    def allow_syncdb(self, db, model):
        """
        Make sure the myapp app only appears on the 'other' db
        """
        if db == 'vpkg':
            return model._meta.app_label == 'vpkg'
        elif model._meta.app_label == 'vpkg':
            return False
        return None
