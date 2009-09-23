import os
import shutil
import sys
import hashlib
import simplejson as json

def rese (path , js):
    lst = os.listdir (path)
    lst2 = list ()
    ret = list ()
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
            
            lst2.append (di)
            
    ret = js[:] + lst2[:]
    return ret 




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
a = rese (url , b)
print json.JSONEncoder().encode (a).replace (',' , ',\n').replace ('},' , '},\n').replace ('"}' , '"\n}').replace ('{"' , '{\n"')










