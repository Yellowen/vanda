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


import codec
import os
import shutil


class RepositoryError (Exception):
    def __init__ (self, err):
        self.errstr = err
    def __unicode__ (self):
        return self.errstr
    def __str__ (self):
        return self.errstr
    


class Repository (object):
    """
    Dina Repository Class
    """

    def __init__ (self, _url, cache, codename="stable", sections=["main", ]):
        self.protocol = _url.split (':')[0]
        self.codec = codec.getCodec (self.protocol)
        if not self.codec :
            raise RepositoryError ("\"%s\" does not support by DPM at this time." % (self.protocol))
        self.codename = codename
        self.sections = sections
        if _url[-1] == "/":
            
            _url = _url[:-1]
        self.url = _url
        self.cache = cache
        self.name = _url.replace (' ', '_').replace ('/', '_')
        
        

    #def _setUrl (self, _url):
        #+++ i should add here an url validation
        
    #    if _url[-1] == "/":
            
    #        _url = _url[:-1]
    #    self.url = _url
        

    #def _getUrl (self):
    #    return self.url
    
    # url = property (fget = _getUrl, fset= _setUrl)




    def _getFile (self, addr):
        """
        Download the given file.
        """
        if not addr:
            return - 1
        filename = addr.split ('/')[-1]
        try:
            self.codec.getFile (self.url + addr, self.cache)
            
        except:
                #+++ here i should add better output
                raise RepositoryError ("codec.getFile : error")
        
        return self.cache + filename


    def update (self):
        """
        Update repository packages file.
        """

        self.CleanCache ()
        
        #+++ here i should add some scurity identification for repositories. something lik Release file in debian

        # Check for repo dir in the cache directory
        if not os.path.exists (self.cache + "repo"):
            pwd = os.getcwd ()
            os.chdir (self.cache)
            # create the repo dir
            os.mkdir ("repo")
            os.chdir (pwd)
        
        # check for its cache dir inside of main cache directory
        if not os.path.exists (self.cache + "repo/" + self.name):
            os.mkdir (self.cache + "repo/" + self.name)
        addr = list ()
        
        # build a dict that contain a url(contain the address of Packages.json file in repository for certain section like main)
        # cache_dir (contain the name of cache directory for a section that live in cache/repo/repo_name/cache_dir)

        for i in self.sections:
            
            addr.append({"url" :  self.url + "/dists/" + self.codename + "/" + i + "/Packages.json", "cache_dir" : self.codename + "_" + i})
            
        dirs = os.listdir (self.cache + "repo/" + self.name)
        for i in addr:
            # Check for exists section cache_dir in main cache directory
            if not i["cache_dir"] in dirs:
                os.mkdir (self.cache + "repo/" + self.name + "/" + i["cache_dir"])
            try:
                # Get the remote Packages.json file and store it in cache
                self.codec.getFile (i["url"], self.cache + "repo/" + self.name + "/" + i["cache_dir"])
            except:
                raise RepositoryError ("codec.getFile : error")


    def CleanCache (self):
        """
        Clean the cache.
        """
        try:
            shutil.rmtree (self.cache + "repo/" + self.name)
        except:
            pass



