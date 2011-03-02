# ---------------------------------------------------------------------------------
#    Dina Project 
#    Copyright (C) 2010  Dina Project Community
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
# ---------------------------------------------------------------------------------

from django import forms
from django.utils.translation import ugettext as _

class ticketform(forms.Form):
    STATUS_CHOICE=(
        ('O','Open'),
        ('C','Close'),
        ('A','Answer'),
        ('Q','Question'),
    )
    title=forms.CharField(max_length=60,verbose_name=_("Title"))
    description=forms.TextField(verbose_name=_("Description"))
    status=forms.CharField(max_length=1,choices=STATUS_CHOICE,verbose_name=_("Status"))
