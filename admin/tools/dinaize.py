#! /usr/bin/env python


#--- JUST A DEVELOPMENT VERSION FOR FAST WORKING
import os 

os.mkdir("dina")

try:
    fd = open ("dina/control" , "w")
except:
    raise "Permission Deniad."

app = dict ()

app["version"] = raw_input ("Version :  ")
app["author"] = raw_input ("Who is author of package? ")

app ["auth_mail"] = raw_input ("What is the email of author? ")
app["home"] = raw_input ("Where is the package home page ? ")
app['url'] = raw_input ("Enter the default URL for the app to listening : ")
app['short'] = raw_input ("Enter one line as its short description : ")


fd.write ("Name = %s;\n" % (os.getcwd ().replace ("\\" , "/").split ("/")[-1]))
for i in app:
    fd.write ("%s = %s;\n" % (i , app[i]))

fd.close ()


