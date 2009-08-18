import os

def load_apps ():
    flist = os.listdir (os.path.dirname (__file__))
    apps = ()
    
    for i in flist:
        if i[-5:-1] == ".conf" :
            #+++ here i should add an error handler after testin
            fd = open (i , 'r')
            lines = fd.readlines ()
            fd.close ()
            apps += ('apps.' + lines[0])
    return apps
            
def load_urls ():
    flist = os.listdir (os.path.dirname (__file__))
    apps = ()
    
    for i in flist:
        if i[-5:-1] == ".conf" :
            #+++ here i should add an error handler after testin
            fd = open (i , 'r')
            lines = fd.readlines ()
            fd.close ()
            apps += (lines[1])
    return apps

