#! /usr/bin/env python
# ---------------------------------------------------------------------------------
#    Dina Project 
#    Copyright (C) 2010  Dina Project Community
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# ---------------------------------------------------------------------------------
import os
import shutil
import tarfile as tf
import sys
import simplejson as json




def parser  (filename):
    """
    Simple parser function that parse a file to a python dict.
    """
    a = dict ()
    try:

        fd = open (filename , 'r')
        st = fd.read ().replace ('\n' , '').split (';')
        
        for i in st:
            #+++ here i should add a validator
            
            key = i.split ('=')[0].strip ().lower()
            value = i.split ('=')[1].strip ().lower()
            a[key] = value
    except IndexError , e :
        pass
        
    except:
        raise "%s : No such file or directory." % (filename)
    return a





def read_file (path):
    path = os.path.abspath (path).replace("\\" , "/") + "/"
    

    pwd = os.getcwd ()
    os.chdir (path + "../")
    attr = parser (path + "dina/control")
    filename = attr['name'] + "-" + attr['version'] + ".tar.bz2"

    try:
        os.mkdir ("/tmp/buildpkg/")
    except:
        pass
    try:
        shutil.copytree (path , '/tmp/buildpkg/' + path.split ('/')[-2])
    except OSError , e:
        pass
        
    shutil.rmtree ('/tmp/buildpkg/' + path.split ('/')[-2] + "/dina")
    fd = tf.open ('/tmp/buildpkg/' + filename , "w:bz2")
    os.chdir ('/tmp/buildpkg/')
    fd.add (path.split ('/')[-2])
    fd1 = open ('/tmp/buildpkg/Package.json' , 'w')
    fd1.write (json.JSONEncoder().encode (attr).replace (',' , ',\n').replace ('},' , '},\n').replace ('"}' , '"\n}').replace ('{"' , '{\n"'))
    fd1.close ()
    fd.add ('Package.json')
    fd.close ()
    shutil.copy ('/tmp/buildpkg/' + filename , path + "../")
    shutil.rmtree ('/tmp/buildpkg')
    os.chdir (pwd)
    


if __name__ == "__main__" :

#+++ optparser should be used instead of this opt patser
    if len (sys.argv) > 1:
        if sys.argv[1][-1] == "/":
            ps = sys.argv[1][:-1]
        else:
            ps = sys.argv[1]
        if os.path.isdir (os.path.join (os.path.dirname (ps) , ps).replace ('\\' , '/')):
            target = sys.argv[1]
        else:
            print "Check first argument for a valid directory."
            sys.exit (1)


    print "Dina CMS toolchain. "
            
    read_file (target)
