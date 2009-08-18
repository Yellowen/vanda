import os
from django.conf.urls.defaults import *


def load_apps ():
    flist = os.listdir (os.path.dirname (__file__))
    app = ()
    
    for i in flist:
        if i[-5:-1] == ".conf" :
            #+++ here i should add an error handler after testin
            fd = open (i , 'r')
            lines = fd.readlines ()
            fd.close ()
            app += ('apps.' + lines[0])
    return app


            
def load_urls ():
    flist = os.listdir (os.path.dirname (__file__))
    apps = ()
    
    for i in flist:
        if i[-5:-1] == ".conf" :
            #+++ here i should add an error handler after testin
            fd = open (i , 'r')
            lines = fd.readlines ()
            fd.close ()
            apps += patterns ('' , (r''+ lines[1] , include ('apps.' + lines[0] + ".urls") ), )
    return apps

