import os
import shutil
import tarfile as tf
import sys

if len (sys.argv) > 1:
    if os.path.isdir ( os.path.join (os.path.dirname (sys.argv[1]) , sys.argv[1]).replace ('\\' , '/')):
        target = sys.argv[1]
    else:
        print "Check first argument for a valid directory."
        sys.exit (1)


#+++ here i should add to way for getting information about app :
#+++ 1 . by askong from user 
#+++ 2 . by reading a file in a directory like dina ( just like debian control directory)

# 1:
def user_get (path):
    pwd = os.getcwd ()
    os.chdir (path)
    dirname = path.split ("/")[-1]
    app = dict ()
    app["author"] = raw_input ("Who is author of package? ")
    app ["auth_mail"] = raw_input ("What is the email of author? ")
    app["home"] = raw_input ("Where is the package home page ? ")
    app['url'] = raw_input ("Enter the default URL for the app to listening : ")
    app['short'] = raw_input ("Enter one line as its short description : ")
    #+++ here i should make desc to act like a text area
    app['desc'] = raw_input ("Enter some text as its description : ")
    
    
    


def read_file (path):
    pwd = os.getcwd ()
    os.chdir (path)




print "dpm-buildpkg tool "

