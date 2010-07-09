"""
Wrapper for loading templates from the filesystem by active template.
"""
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



from django.conf import settings
from django.template import TemplateDoesNotExist
from django.template.loader import BaseLoader
from django.utils._os import safe_join

from dina.cache import Template 
from dina.log import Logger
from dina.fem.layout.parser import Parser

# IMPORTANT: --------------------------------------------------------
# This import section may change in the due to finding a better
# Tree structur 
#from dina.DPM.models import Template
from dina.fem.template.parser import ParseBase , FillSections
# ------------------------------------------------------------------

class Loader(BaseLoader):
    is_usable = True
    temp_index = []
    logger = Logger ("FS template loader")
    def get_template_sources(self, template_name, template_dirs=None):
        """
        Returns the absolute paths to 'template_name', when appended to each
        directory in 'template_dirs'. Any paths that don't lie inside one of the
        template dirs are excluded from the result set, for security reasons.
        """
        
        
        if not template_dirs:
            template_dirs = settings.TEMPLATE_DIRS
            
        for template_dir in template_dirs:
            try:

                active_template = Template.current_template_dir ()
                template_n = active_template + template_name
                
                
                yield safe_join(template_dir, template_n)
                
            except UnicodeDecodeError:
                # The template dir name was a bytestring that wasn't valid UTF-8.

                raise
            except ValueError:
                # The joined path was located outside of this particular
                # template_dir (it might be inside another one, so this isn't
                # fatal).
                pass

    # TODO: Find a good way to allow user to use section tag in any html file
    def load_template_source(self, template_name, template_dirs=None):
        tried = []
        for filepath in self.get_template_sources(template_name, template_dirs):

            try:
                
                
                template_data, cached_template = Template.get_template (filepath, template_name)
                
                
                if cached_template:
                    return (template_data, filepath)
                else:
                    parser = Parser (template_data)
                    replaced_template_data = parser.parse_data ()
                    return (replaced_template_data, filepath)
#                try:

                 #   if template_name == "base.html":
                        
                 #       unparse_template = ParseBase ("/".join (filepath.split("/")[:-1]),\
                 #template_name)
                 #       if unparse_template is None:
                            
                 #           unparse_template = file.read().decode(settings.FILE_CHARSET)
                        #unparse_template = FillSections (unparse_template)
                 #   else:

#                        unparse_template = file.read().decode(settings.FILE_CHARSET)

 #                       return (unparse_template , filepath)
  #              finally:
   #                 file.close()
            except IOError:
                tried.append(filepath)
        if tried:
            error_msg = "Tried %s" % tried
        else:
            error_msg = "Your TEMPLATE_DIRS setting is empty. Change it to point to at least one template directory."
        raise TemplateDoesNotExist(error_msg)
    load_template_source.is_usable = True

_loader = Loader()

def load_template_source(template_name, template_dirs=None):
    # For backwards compatibility
    import warnings
    warnings.warn(
        "'django.template.loaders.filesystem.load_template_source' is deprecated; use 'django.template.loaders.filesystem.Loader' instead.",
        PendingDeprecationWarning
    )
    return _loader.load_template_source(template_name, template_dirs)
load_template_source.is_usable = True
