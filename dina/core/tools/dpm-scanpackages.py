#! /usr/bin/env python
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
        # Check the i (that is a file or directory) for being directory
        if os.path.isdir (os.path.join (os.path.dirname (path + "/"  + i) , i).replace ('\\' , '/')):

            # if it is then call this function again with new path that is i
            lst2 = lst2[:] + rese (path + "/" + i + "/", js)[0][:]
        else:

            #if it is not . then parse the file name for name version.
            di = dict () 
            name = i.split("-")[0]
            di["Package"] =  name
            version = ".".join (i.split ("-")[1].split(".")[:3])
            di["Version"] =  version
            # Generate the SHA1 hash for package for its validation in future
            m = hashlib.sha1 ()
            m.update (file (path + "/" + i , 'r').read())
            di["SHA1"] = m.hexdigest ()
            # address element will point to package file , and store to Packages.json file
            di["Address"] = os.path.join (os.path.dirname (path + "/" + i) , i).replace ('\\' , '/')
            # Open the packege file for gathering more information from package
            fd = tf.open (os.path.join (os.path.dirname (path + "/"  + i) , i).replace ('\\' , '/'))
            try:
                # extract the Package.json file in /tmp
                try:
                    os.mkdir ('/tmp/dpm_pkg')
                    os.mkdir ('/tmp/dpm_pkg/' + i)
                except:
                    pass
                fd.extract ("Package.json" , "/tmp/dpm_pkg/" + i + "/")
                fd.close ()
                try:
                    # Try to read the json content
                    ff = open ("/tmp/dpm_pkg/" + i + "/Package.json")
                    acc =  ff.read ().lower()
                    
                    ff.close ()
                    jobj = json.loads (acc + "\n")
                    
                except :
                    
                    
                    raise JSONError ("your Package.json file in %s has a syntax error." % (i + "/Package.json"))
                    #+++ here i should add a try/except for doesn't exists keys
                    
                di["Author"] = jobj["author"]
                di["Home"] = jobj["home"]
                di["Email"] = jobj["email"]
                
                    #+++ maybe i should escape the url value
                
                di["Short_Desc"] = jobj["short"]
                #di["Desc"] = jobj[0]["desc"]
                
                    
                if jobj["type"] == "application" or jobj["type"] == "template":
                    di["Type"] = jobj["type"]
                    if jobj["type"] == "application":
                        di["Url"] = jobj["url"]
                else:
                    raise JSONError ("Package.json -> Type should be Application or Template.")



                
            except IOError , e:
                brk.append (os.path.dirname (path + "/" + i) , i).replace ('\\' , '/')
            
            lst2.append (di)
            
    #ret = js[:] + lst2[:]
    ret =  lst2[:]
    
    #return the Packages json content
    return [ret , brk]




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
[a , c]  = rese (url , b)
shutil.rmtree ('/tmp/dpm_pkg/')
if len (c) > 0 :
    print "dpm-scanpackages find some broken packages:"
    for i in c:
        print "___C " +  i

    print "Check Package.json file inside of packages for valid JSON formation or existance."
else:
    #print "------> " + a
    print json.JSONEncoder().encode (a).replace (',' , ',\n').replace ('},' , '},\n').replace ('"}' , '"\n}').replace ('{"' , '{\n"')










