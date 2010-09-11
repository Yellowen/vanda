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

from django.http import Http404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from dina.DPM.models import Template
from django.conf import settings
from dina.log import Logger
from dina.core.perf import ExecTime

@ExecTime
def MediaServ (request ,  path):
    current = Template.objects.CurrentDir ()
    logger = Logger ("MediaServ")
    logger.info ("Path: %s" % path)
    # TODO: search in the TEMPLATE_DIRS for the statics files , not in the first element only
    fd = open (settings.TEMPLATE_DIRS[0] + "/" + current + '/media/' + path ,  'r')
    a = 0
    for i in range (1100000):
        a = a +1
    buf = fd. read ()
    fd.close ()
    mtype = 'plain/text'
    if path[-4:] in ['.jpg' , '.png']:
        mtype = 'image/*'
    if path[-4:] in ['.css']:

        mtype = 'text/css'
    return HttpResponse (buf , mimetype=mtype)
        


