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
import random
import simplejson as json
from django.conf import settings
from repository import *
from models import Repo as rp
from models import application , template
import bz2


class DPMError (Exception):
    
    def __init__ (self , err):
        self.errstr = err
    def __unicode__ (self):
        return self.errstr
    def __str__ (self):
        return self.errstr




class DPM (object):
    """
    Dina Package manager.
    """
    
    def __init__ (self ):
        
        # Setting up cache directory path
        if settings.DPM_CACHE :
            if settings.DPM_CACHE[-1] != "/":
                self.cache = settings.DPM_CACHE + "/"
            else:
                self.cache = settings.DPM_CACHE
        else:
            self.cache = '/tmp/'

        self.id = random.randrange (100 ,200)
        
        # retrive all repositories
        confs = rp.objects.all ()
        # parse the repositories information
        self._repositories = self._sourceparser (confs)
        


    def _sourceparser (self , conflist):
        """
        Parse the source list for repositories.
        """

        #+++ may be i write a better parser
        repos = list ()
        
        for i in conflist:
            
            url =i.url.split (' ')[0]
            try:
                codename = i.url.split (' ')[1]
            except:
                codename = "stable"
            sections =i.url.split (' ')[2:]
            repos.append (Repository (url , self.cache , codename , sections ))
            return repos




    def update (self , repo='all'):
        """
        Update the Packages file of given repository. and cache the packages file
       """
        # call the update method for repo
        for i in self._repositories:
            if repo == 'all':
                i.update ()
            elif repo == i.name:
                i.update ()
                
        pkgs = dict ()
        # load the Packages list from cached files
        for i in self._repositories:
            addr = self.cache + "repo/" + i.name
            
            dirs = os.listdir ( addr )
            for j in dirs:
                
                if j[0] == '.':
                    # skip the hidden dirs
                    pass
                else:
                    # open the cached Packages.json for a section
                    fd = open (addr + "/" + j + "/Packages.json")
                    # load its json content into a python dict
                    jobj = json.loads (fd.read ().lower ())
                    fd.close ()
                    tmppkgs = dict ()

                    for y in jobj :
                        #+++ here i should add extra dara this is just for basic usage
                        pname = y["package"]
                        psha1 = y["sha1"]
                        pversion = y["version"]
                        paddress = y["address"]
                        shortdesc = y["short_desc"]
                        #desc = y["desc"]
                        
                        # skip the exist packages by checking for exists hashes
                        if tmppkgs.has_key (psha1):
                            pass
                        else:
                            # provide a cache for for package information in above format
                            tmppkgs[psha1] = pname  + "::" + psha1 + "::" + pversion + "::" + paddress + "::" + shortdesc
                    
                            
                    l1  = list (set (pkgs ) ^ set (tmppkgs))
                    
                    l2  = list (set (pkgs ) ^ set (l1))

                    diffs = list ()
                    if len (l2) > 0:
                        diffs = l1 + l2
                    else:
                        diffs = l1
                    tmp = dict()
                    for i in diffs:
                        if pkgs.has_key (i):
                            tmp[i] = pkgs[i]
                        elif tmppkgs.has_key (i):
                            tmp[i] = tmppkgs[i]
                    # final packages list
                    pkgs = tmp


                    
        pkgs_namelist = list ()
        for i in pkgs:
            phash = pkgs[i].split("::")[1]
            try:
                # check for installed application
                app = application.objects.get (SHA1=phash)
                app = "*"
            except:
                try:
                    # check for install template
                    app = template.objects.get (SHA1=phash)
                    app = "*"
                except:
                    app = "!"
                
                    
            
            
            #pkgs_namelist.append (str (pkgs[i].split("::")[0]) + "::" + app)
            pkgs_namelist.append (str (pkgs[i] + "::" + app))
        pkgs_namelist.sort ()

        

        # write cache data to files
        fd = open (self.cache + "Packages" , 'w')
        for i in pkgs:
            fd.write (pkgs[i] + "\n")
        fd.close ()
        fd = open (self.cache + "pkgs.cache" , "w")
        for i in pkgs_namelist:
            fd.write (i + "\n")
        fd.close ()

                    
                        
        






    def pkglist (self , section="all"):
        """
        Return the packages list in given category.
        """
        try:
            fd = open (self.cache + "pkgs.cache" , 'r')
            pkgs = fd.readlines ()
            fd.close ()
            
            return [i.replace ("\n" , "") for i in pkgs]
        except:
            raise DPMError ('Update needed.')
    



    def install (self , pkglist):
        """
        Installer a Package list.
        """

        # Checking for other DPM process by lock file
        try:
            fd = open (self.cache + "lock"  , 'r')
            oid = fd.read ()
            fd.close ()
            raise DPMError ("An other DPM process with '%s' ID running." % (oid))
        except:
            # lock the repository
            fd = open (self.cache + "lock"  , 'w')
            fd.write (str (self.id))
            fd.close ()

        # Check for exists pkgs dir in cache directory
        if not os.path.exists (self.cache + "pkgs"):
            os.mkdir (self.cache + "pkgs")
        
        
        
    def show (self , mhash):
        """
        Return a dictionary that contain package information.
        """
        bz = bz2.BZ2Compressor ()
        fd = open (self.cache + "pkgs.cache")
        lst = fd.readlines ()
        fd.close ()
        for i in lst :
            phash = i.split ("::")[1]
            if phash == mhash:
                return {"name" : i.split ("::")[0] , "hash" : phash , "version" : i.split ("::")[2] , "short" : i.split ("::")[4] } # , "desc" : bz.decompress (i.split ("::")[6]) }
        
        
        

