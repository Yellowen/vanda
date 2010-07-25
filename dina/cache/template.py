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

import pickle

from dina.DPM.models import Template
from base import CacheObject
from dina.log import Logger
from dina.core.utils import modification_date , date_cmp

logger = Logger ('Template cache class')


        



class TemplateQueryCache (CacheObject):
    """
    This class will cache the Template model in DPM package for decreasing
    number of queries in Dina actions.
    """
    

    def __init__ (self):
        super(TemplateQueryCache, self).__init__ ("templates")
        self.template = Template.objects.get (Active=True)

        # load and parse the .modifies file inside of the template cache dir
        # that contains some data about the latest modified time for templates
        # that cached.
        # .modifies file format are as follow:
        # templatename::time
        self.pkl = "modifies.pkl"
        self.modifies = dict()
        try:
            fd = open ("%s/%s" % (self._cache_dir, self.pkl))
            self.modifies = pickle.load (fd)
            fd.close ()
        except IOError:
            pass

                       
        # TODO: add a config or a settings option that allow memory caching for
        # templates
        self.memcache = None
        self.cache = {}
        logger.debug ("TemplateQueryCache class inti.")
        logger.info ("Current active template is %s" % self.template)

    def current (self):
        return self.template

    def current_template_dir (self):
        return "%s/" % self.template.Name



    def get_template (self, address, template_name):
        """
        Try to return the cache data for given template if there was any in
        <DINA_CACHE>/templates/<escaped TEMPLATE_NAME>/
        escaped TEMPLATE_NAME is the same as TEMPLATE_NAME but '/' characters
        replaced by '___' and comes with a '.cache' suffix
        otherwise return the normal file data.
        """
        fdate = modification_date (address)
        if self.modifies.has_key(template_name):
            if date_cmp (self.modifies[template_name], fdate) == 0:
                # no need to reparse the template, there is a up2date cache before
                logger.info ("Reading %s from cache." % template_name)
                return (self._read_cache (template_name),  True)
                
            else:
                
                cache_fd = open (address)
                cache_data = cache_fd.read ()
                cache_fd.close ()
                logger.info ("Reading %s from FS." % template_name)
                return (cache_data, False)
        else:
            cache_fd = open (address)
            cache_data = cache_fd.read ()
            cache_fd.close ()
            logger.info ("Reading %s from FS." % template_name)
            logger.info ("%s" % cache_data)
            return (cache_data, False)


        
    def _cache_template (self , templatename):
        pass

    def write_cache (self, absolute_path, filename, data):
        """
        build a cache file for given filename and write data in it.
        """

        fdate = modification_date (absolute_path)
        self.modifies[filename] = fdate
        fd = open ("%s/%s" % (self._cache_dir, self.pkl) , 'w+')
        pickle.dump (self.modifies, fd)
        fd.close ()
        self._write_cache (filename, data)
        logger.info ("%s template cached." % filename)
    
