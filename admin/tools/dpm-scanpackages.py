import os
import shutil
import sys
import hashlib
import tarfile as tf
import simplejson as json

class JSONError (Exception):
    def __init__ (self , err):
        print "JSON Error : " + err


def rese (path , js):
    lst = os.listdir (path)
    lst2 = list ()
    ret = list ()
    brk = list ()
    for i in lst:
        
        if os.path.isdir (os.path.join (os.path.dirname (path + "/"  + i) , i).replace ('\\' , '/')):
            
            lst2 = lst2[:] + rese (path + "/" + i + "/", js)[:]
        else:
            di = dict () 
            name = i.split("-")[0]
            di["Package"] =  name
            version = ".".join (i.split ("-")[1].split(".")[:3])
            di["Version"] =  version
            m = hashlib.sha1 ()
            m.update (file (path + "/" + i , 'r').read())
            di["SHA1"] = m.hexdigest ()
            di["Address"] = os.path.join (os.path.dirname (path + "/" + i) , i).replace ('\\' , '/')
            fd = tf.open (os.path.join (os.path.dirname (path + "/"  + i) , i).replace ('\\' , '/'))
            try:
                os.mkdir ('/tmp/dpm_pkg')
                fd.extract (i + "/Package.json" , "/tmp/dpm_pkg")
                try:
                    jobj = json.loads (file ("/tmp/dpm_pkg/" + i + "/Package.json").read ().lower())
                except:
                    raise JSONError ("your Package.json file in %s has a syntax error." % (i + "/Package.json"))
                    #+++ here i should add a try/except for doesn't exists keys
                    
                di["Author"] = jobj[0]["author"]
                di["Home"] = jobj[0]["home"]
                di["Email"] = jobj[0]["email"]
                
                    #+++ maybe i should escape the url value
                di["Url"] = jobj[0]["url"]
                di["Short_Desc"] = jobj[0]["short_desc"]
                di["Desc"] = jobj[0]["desc"]
                
                    
                if jobj[0]["type"] == "app" or jobj[0]["type"] == "theme":
                    di["Type"] = jobj[0]["type"]
                else:
                    raise JSONError ("Package.json -> Type should be app or theme.")



                
            except IOError , e:
                brk.append (os.path.dirname (path + "/" + i) , i).replace ('\\' , '/'))
            
            lst2.append (di)
            
    ret = js[:] + lst2[:]
    shutil.rmtree ('/tmp/dpm_pkg')
    return ret , brk




if  len (sys.argv) == 1:
    print "\nUsage : pkg-scan.py path_to_pool_dir\n"
    sys.exit (1)

url = sys.argv[1]

if url == "help":
    print "\nUsage : pkg-scan.py path_to_pool_section_dir"
    print "path_to_pool_section_dir should point to section dir for example:"
    print "$ pkg-scan.py /home/pool/main\n"
    sys.exit(0)

if url[-1] == "/":
    url = url[:-1]

b = list ()
a , c  = rese (url , b)
if len (c) > 0 :
    print "dpm-scanpackages find some broken packages:"
    for i in c:
        print i

    print "Check Package.json file inside of packages for valid JSON formation or existance."
else:
    print json.JSONEncoder().encode (a).replace (',' , ',\n').replace ('},' , '},\n').replace ('"}' , '"\n}').replace ('{"' , '{\n"')










