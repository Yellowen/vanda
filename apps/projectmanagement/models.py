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



class ProjectManagement(models.Model):
    author=models.ForeignKey("auth.User" , editable = True , verbose_name=_("User"))
    title=models.CharField(max_length=30 , verbose_name=_("Project Title"))
    defineDate=models.DateField(verbose_name=_("Define Date"))
    startDate=models.DateField(blank=True , null = True ,verbose_name=_("Start Date"))
    outDate=models.DateField(blank = True , null = True ,verbose_name=_("Date Out"))
    terminateDate=models.DateField(blank = True , null = True ,verbose_name=_("Terminate Date"))
    subProject=models.ForeignKey("ProjectManagement" , blank = True , null = True)
    
    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        return "/project/%s" % self.id
