#! /usr/bin/env python
# ---------------------------------------------------------------------------------
#    Dina Project 
#    Copyright (C) $YEAR$  $AUTHOR$
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

#--- JUST A DEVELOPMENT VERSION FOR FAST WORKING
import os 

try:
    os.mkdir("dina")
except:
    pass

try:
    fd = open ("dina/control" , "w")
except:
    raise "Permission Deniad."

app = dict ()
a = 1
pl = ""
while (a == 1):
    ac = raw_input ("Type (1=Application , 2=Template) :  ")
    if ac == "1" or ac == "2":
        if ac == "1":
            print ac
            pl = "Application"
        else:
            print ac
            pl = "Template"
        a = 0
       
app["type"] = pl
app["version"] = raw_input ("Version :  ")

app["author"] = raw_input ("Who is author of package? ")

app ["email"] = raw_input ("What is the email of author? ")
app["home"] = raw_input ("Where is the package home page ? ")
if app['type'] == "Application":
    app['url'] = raw_input ("Enter the default URL for the app to listening : ")
app['short'] = raw_input ("Enter one line as its short description : ")


fd.write ("Name = %s;\n" % (os.getcwd ().replace ("\\" , "/").split ("/")[-1]))
for i in app:
    fd.write ("%s = %s;\n" % (i , app[i]))

fd.close ()


