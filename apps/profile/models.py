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

class UserProfile(models.Model):
	author = models.ForeignKey ("auth.User" , unique=True , editable = True , verbose_name = _("Author"))
	nickname = models.CharField(unique=True  ,max_length = 30 ,verbose_name=_("Nickname"))
	description = models.TextField(null=True ,blank = True ,verbose_name = _("Discription's"))
	birthday = models.DateField(null=True ,blank = True ,verbose_name = _("Birthday"))
	picture = models.ImageField(null=True ,blank = True ,upload_to="/Profile/")
	
	def __unicode__ (self):
		return self.nickname

