# -----------------------------------------------------------------------------
#    Dtable - data table application for Vanda platform
#    Copyright (C) 2012 Some Hackers In Town
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
from django.db import models


class DTModel(models.Model):

    @staticmethod
    def get_class_dict(self, fields, tableobj=None):
        values_dict = {}
        for field in fields:
            field_name = field.split(".")[0]
            if hasattr(self, field_name):
                values_dict[field_name] = self
                for prop in field.split("."):
                    values_dict[field_name] = getattr(values_dict[field_name],
                                                      prop)

                if callable(values_dict[field_name]):
                    values_dict[field_name] = values_dict[field_name]()
                else:
                    values_dict[field_name] = unicode(values_dict[field_name])
            else:
                if tableobj:
                    if hasattr(tableobj, field_name):
                        values_dict[field_name] = tableobj
                        for prop in field.split("."):
                            values_dict[field_name] = getattr(
                                values_dict[field_name],
                                prop)

                        if callable(values_dict[field_name]):
                            values_dict[field_name] = values_dict[
                                field_name](self)
                        else:
                            values_dict[field_name] = unicode(
                                values_dict[field_name])
                else:
                    raise ValueError("'%s' or DTable classes does not have '%s' attr." % (
                        self.__class__.__name__,
                        field))

        return values_dict

    def get_dict(self, fields, tableobj=None):
        values_dict = {}
        for field in fields:
            field_name = field.split(".")[0]
            if hasattr(self, field_name):
                values_dict[field_name] = self
                for prop in field.split("."):
                    values_dict[field_name] = getattr(values_dict[field_name],
                                                      prop)

                if callable(values_dict[field_name]):
                    values_dict[field_name] = values_dict[field_name]()
                else:
                    values_dict[field_name] = unicode(values_dict[field_name])
            else:
                if tableobj:
                    if hasattr(tableobj, field_name):
                        values_dict[field_name] = tableobj
                        for prop in field.split("."):
                            values_dict[field_name] = getattr(
                                values_dict[field_name],
                                prop)

                        if callable(values_dict[field_name]):
                            values_dict[field_name] = values_dict[
                                field_name](self)
                        else:
                            values_dict[field_name] = unicode(
                                values_dict[field_name])
                else:
                    raise ValueError("'%s' or DTable classes does not have '%s' attr." % (
                        self.__class__.__name__,
                        field))

        return values_dict

    class Meta:
        abstract = True
