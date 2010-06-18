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

import logging
import os
from django.conf import settings

logparam = {'filemode' : 'w'}

try:
    logparam['level'] = settings.LOG_LEVEL
except AttributeError:
    pass

try:
    logparam['format'] = settings.LOG_FORMAT
except AttributeError:
    pass

try:
    logparam['datefmt'] = settings.LOG_DATE_FORMAT
except AttributeError:
    pass

try:
    if not os.path.exists (settings.LOG_FILE):
        fd = open (settings.LOG_FILE, 'w')
        fd.close ()
        
    logparam['filename'] = settings.LOG_FILE
            
except AttributeError:
    pass

try:
    logparam['filemode'] = settings.LOG_FILE_MODE
except AttributeError:
    pass


logging.basicConfig(**logparam)

Logger = logging.getLogger



