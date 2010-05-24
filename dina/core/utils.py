# ---------------------------------------------------------------------------------
#    Dina Project 
#    Copyright (C) 2010  Dina Project Developer Community
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

import os
import datetime


# Return the last modification date for give file name
def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t).replace (" " , "-").replace (":","-")


# Compare fdate with sdate. if fdate was greater than sdate result = 1
# if sdate greater that fdate result = 2
# if fdate and sdate was equal result = 0
# fdate and sdate should be string type date that seprated by '-' char
def date_cmp (fdate, sdate):
    flist = fdate.split ("-")
    slist = sdate.split ("-")
    for i in len(flist):
        if flist[i] > slist[i]:
            return 1
        elif flist[i] < slist[i]:
            return 2
    return 0


