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



class AddressBook(models.Model):
	ADDRESS_TYPE_CHOICES = (
        ('H', 'Home'),
        ('W', 'Work')
	)
	author = models.ForeignKey("auth.User")
	street = models.CharField(max_length=30 , verbose_name=_("Street"))
	
	# TODO: chenge city field to choice list for saving integration in user version
	
	city = models.CharField(max_length=30 , verbose_name=_("City"))
	state = models.CharField(max_length=30 , verbose_name=_("State"))
	zipCode = models.CharField(max_length=10 , verbose_name=_("Zip Code"))
	
	
	# TODO: chenge contry field to choice list for saving integration in user version
	
	country = models.CharField(max_length=30 , verbose_name=_("Country"))
	addressType = models.CharField(max_length=1 , choices = ADDRESS_TYPE_CHOICES , verbose_name=_("Address Type"))
	
	def __unicode__(self):
		return "%s" % self.street + " ," + self.city + " ," + self.state + " ," + self.country
	
	def get_absolute_url(self):
		return "/addressbook/%s" % self.id
