import os
import shutil
import tarfile as tf
import sys
import simplejson as json


if len (sys.argv) > 1:
    if os.path.isdir ( os.path.join (os.path.dirname (sys.argv[1]) , sys.argv[1]).replace ('\\' , '/')):
        target = sys.argv[1]
    else:
        print "Check first argument for a valid directory."
        sys.exit (1)




def parser  (filename):
    a = dict ()
    try:

        fd = open (filename , 'r')
        st = fd.readline ().split (';')
        for i in st:
            #+++ here i should add a validator
            key = i.split ('=')[0].strip ().lower()
            value = i.split ('=')[1].strip ().lower()
            a[key] = value
    except:
        raise "%s : No such file or directory." % (filename)
    return 0



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
    os.chdir (path + "../")
    attr = parser (path + "/dina/control")
    filename = attr['name'] + "-" + attr['version'] + ".tar.bz2"
    try:
        os.mkdir ("/tmp/buildpkg/")
    except:
        pass
    shutil.copy (path , '/tmp/buildpkg/')
    os.rmdir ('/tmp/buildpkg/' + path.split ('/')[-1] + "/dina")
    fd = tf.open ('/tmp/buildpkg/' + filename , "w:bz2")
    fd.add ('/tmp/buildpkg/' + path.split ('/')[-1])
    fd1 = open ('/tmp/buildpkg/Package.json' , 'w')
    fd1.write (json.JSONEncoder().encode (attr).replace (',' , ',\n').replace ('},' , '},\n').replace ('"}' , '"\n}').replace ('{"' , '{\n"'))
    fd1.close ()
    fd.add ('/tmp/buildpkg/Package.json')
    fd.close ()
    shutil.copy ('/tmp/buildpkg/' + filename + ".tar.bz2" , path + "../")


print "dpm-buildpkg tool "

