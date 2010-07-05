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



class PhoneBook(models.Model):
	NUMBER_TYPE_CHOICES = (
        ('H', 'Home'),
        ('W', 'Work'),
        ('M', 'Mobile'),
        ('F', 'Fax'),
        ('P', 'Pager'),                     
	)
	author = models.ForeignKey("auth.User" , editable = True , verbose_name = _("Author")) 
	numberType = models.CharField(max_length=1 , choices=NUMBER_TYPE_CHOICES , verbose_name=_("Number Type"))
	number = models.CharField(max_length=13 , verbose_name=_("Phone Number"))
	
	
	
	def __unicode__(self):
		return "%s" % self.numberType + " : " + self.number
	
	def get_absolute_url(self):
		return "/phonebook/%s" % self.id
