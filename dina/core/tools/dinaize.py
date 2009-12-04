#! /usr/bin/env python


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


