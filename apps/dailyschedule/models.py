# ---------------------------------------------------------------------------------
#    Dina Project 
#    Copyright (C) 2010  Dina Project
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


from django.db import models
from django.utils.translation import ugettext as _





class dailySchedule(models.Model):
    PRIORITY_CHOISE=(
        ('G','Green'),
        ('R','Red'),
        ('Y','Yellow'),
        )
    STATUS_CHOICE=(
        ('O','Open'),
        ('C','Close'),
        ('M','Move to next day'),
        )
    author=models.ForeignKey("auth.User",verbose_name=_("Author"))
    order=models.IntegerField(verbose_name=_("Order"))
    priority=models.CharField(max_length=1,choices=PRIORITY_CHOISE,verbose_name=_("Priority"))
    description=models.TextField(verbose_name=_("Description"))
    result=models.TextField(verbose_name=_("Result"))
    date=models.DateField(verbose_name=_("Date"))
    status=models.CharField(max_length=1,choices=STATUS_CHOICE,verbose_name=_("Status"))
    
    def __unicode__(self):
        return self.description
