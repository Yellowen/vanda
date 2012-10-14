# -----------------------------------------------------------------------------
#    Vanda Core - Vanda core utilities
#    Copyright (C) 2011 Sameer Rahmani <lxsameer@gnu.org>
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
import time
import datetime

from django import forms
from django.core import validators
from django.utils import formats


class JDateField(forms.DateField):
    """
    Jalali DateField
    """

    def __init__(self, *argc, **kwargs):
        super(JDateField, self).__init__(*argc, **kwargs)

    def to_python(self, value):
        """
        Validates that the input can be converted to a date. Returns a Python
        datetime.date object.
        """
        if value in validators.EMPTY_VALUES:
            return None
        if isinstance(value, datetime.datetime):
            return value.date()
        if isinstance(value, datetime.date):
            return value
        for format in self.input_formats or \
                formats.get_format('DATE_INPUT_FORMATS'):
            try:
                print ">>> ", format, time.strptime(value, format)[:3]
                return datetime.date(*time.strptime(value, format)[:3])
            except ValueError:
                continue
        raise ValidationError(self.error_messages['invalid'])
