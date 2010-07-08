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

import re

from django.utils._os import safe_join
from django.conf import settings

from dina.core.utils import modification_date , date_cmp
from dina.DPM.models import Template
from dina.cache import Template as template_cache
from dina.fem.layout.models import TemplateLayout


class Parser (object):
    """
    Template parser for Dina
    """


    def __init__ (self, template_data):
        
        self.lines = template_data.split("\n")
        self.result = template_data
        self.tag_pattern = re.compile ("{% section ('|\")[a-zA-Z0-9_\-]+('|\") %}")
        self.section_name_pattern = re.compile ("('|\")[a-zA-Z0-9_\-]+('|\")")
        self.sections = []

    def parse_data (self):
        """
        parsing template data and searching for section tags
        and build a dictionary from them.

        section tag should be like:

           {% section 'section name' %}
           
        Note: this section tag formation belong to version 0.2 of dina.
        """
        for line in self.lines:
           
            # TODO: find a better way to deal with to section tag in a single line
            tag = self.tag_pattern.search (line)
            if tag is not None:
                print "----> " , line[tag.start(): tag.end ()]
                section = self.section_name_pattern.search (line[tag.start(): tag.end ()])
                if section is not None:
                    # sections will contain the name of sections
                    sec = line[tag.start(): tag.end ()][section.start () +1: section.end () -1]
                    print ">>> " , sec
                    self.sections.append (sec)
                    try:
                        active_template = template_cache.current ()
                        layout = TemplateLayout.objects.get (Section=sec, Template=active_template)
                        tmp = list ()
                        for content in layout.Contents.all ():
                            tmp.append ('%s %s %s %s' % ("{%", content, " ".join(content.Params.split("::")),\
                                                   "%}"))
                        pattern = re.compile ("%s section ('|\")%s('|\") %s" % \
                                              ("{%", sec, "%}"), re.I)
                        self.result = re.sub (pattern,"\n".join (tmp), self.result, 0)
                    except TemplateLayout.DoesNotExist:
                        pattern = re.compile ("%s section ('|\")%s('|\") %s" % \
                                                        ("{%", sec, "%}"), re.I)
                        self.result = re.sub (pattern," \n", self.result, 0)

                    print "-------> Result: " , self.result
                else:
                    # TODO: better exception raising
                    raise "section without name."

 
    def ireplace (self, pattern, old, new, count=0):
        """
        Case-insensitive replace.
        """
        pattern = re.compile(re.escape(old),re.I)
        return re.sub(pattern,new,self,count)

        
