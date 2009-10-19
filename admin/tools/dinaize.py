#! /usr/bin/env python


#--- JUST A DEVELOPMENT VERSION FOR FAST WORKING
import os 

os.mkdir("dina")

try:
    fd = open ("dina/control" , "w")
except:
    raise "Permission Deniad."

app = dict ()

while (1):
    app["type"] = raw_input ("Type (1=Application , 2=Template) :  ")
    if app["type"] == 1 or app["type"] == 2:
        if app["type"] == 1:
            app["type"] == "Application"
        else:
            app["type"] == "Template"
        break
app["version"] = raw_input ("Version :  ")

app["author"] = raw_input ("Who is author of package? ")

app ["email"] = raw_input ("What is the email of author? ")
app["home"] = raw_input ("Where is the package home page ? ")
app['url'] = raw_input ("Enter the default URL for the app to listening : ")
app['short'] = raw_input ("Enter one line as its short description : ")


fd.write ("Name = %s;\n" % (os.getcwd ().replace ("\\" , "/").split ("/")[-1]))
for i in app:
    fd.write ("%s = %s;\n" % (i , app[i]))

fd.close ()


