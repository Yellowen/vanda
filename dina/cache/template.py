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



from dina.DPM.models import Template
from base import CacheObject
from dina.log import Logger

logger = Logger ('Template cache class')

class TemplateQueryCache (CacheObject):
    """
    This class will cache the Template model in DPM package for decreasing
    number of queries in Dina actions.
    """

    def __init__ (self):
        super(TemplateQueryCache, self).__init__ ("templates")
        self.template = Template.objects.get (Active=True)

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
        
        cache_data = self._read_cache (template_name)
        if cache_data is None:
            cache_fd = open (address)
            cache_data = cache_fd.read ()
            cache_fd.close ()
            return (cache_data, False)
        else:
            return (cache_data, True)

        
    def _cache_template (self , templatename):
        pass

    
