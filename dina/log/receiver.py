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

from dina.log import Logger
from dina.code.signals import *

logger = Logger ('Receiver')

dina_init_done.connet (Receiver)

def Receiver (sender, **kwargs):
    """
    General Receiver for all dina core signals.
    """
    tmp = "Sender: <%s> " % sender
    for i in kwargs:
        tmp = tmp + "%s : %s " % (i, kwargs[i])

    print "asdasdadadasdadadasddddddddddddddddddddddddddddddddddddd"
    logger.info (tmp)
