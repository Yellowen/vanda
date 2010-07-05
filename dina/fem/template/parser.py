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

from dina.core.utils import modification_date , date_cmp
from django.utils._os import safe_join
from django.conf import settings


from dina.DPM.models import Template
from dina.fem.layout.models import TemplateLayouts

class TemplateSyntaxError (Exception):
    def __init__ (self, line , char):
        super(TemplateSyntaxError, self).__init__ ("Invalide syntax: '%s' char: %s." % (line , char))



class Section (object):

    def __init__ (self,  **params):
        self.Name = params["name"]
        self.Width = params["width"]
        self.Height = params["height"]
        self.params = params["parameters"]


# TODO: should complete in future for parsing base.html file
class TemplateParser (object):
    """
    this class provide a simple template tag parser that allow dina
    to fill the specific position of a template.
    """


    def __init__ (self, baseaddress , basefile):
        """
        """
        pass
    def __FindSectionTag (self , line):
        # TODO: check for exists section tag, if not skip
        open_tags = line.split (self.OPENMARK)
        if len (open_tags) == 1:
            a = open_tags[0].find (self.CLOSEMARK)
            if not a == -1:
                raise TemplateSyntaxError (line , a)
        else:
            result = list ()
            for i in open_tags[1:]:
                close_mark_position = i.find (self.CLOSEMARK)
                if close_mark_position == -1:
                    raise TemplateSyntaxError (line , "unclosed tag")

                # TODO: chack for space after open mark
                # TODO: check for parsing section tag
                tag = i[:close_mark_position]
                tag = tag.split (" ")
                if tag[1].lower () == "section":
                    tagdic["name"] = tag[2]
                    tagdic[""] = tag[1]
                                           
        

    def getSections (self):
        """
        this method return a list of Section instance that contain the name of each template section with
        the possible properties.
        """
        result = list ()
        for line in self.temlate :
            section = self.__FindSectionTag (line)
            if section:
                result.append (Section (**section))
        return result
    
# TODO: this function is temporary and will remove with HTMLParser
# as soosn as possible
def tmp_BaseParser (template_stream):

    lines = template_stream.split ("\n")
    tag_pattern = re.compile ("{% section ('|\")[a-zA-Z0-9_\-]+('|\") %}")
    section_name_pattern = re.compile ("('|\")[a-zA-Z0-9_\-]+('|\")")
    values =list ()
    for line in lines:

        # TODO: find a better way to deal with to section tag in a single line
        tag = tag_pattern.search (line)
        if tag is not None:
            
            section = section_name_pattern.search (line[tag.start(): tag.end ()])
            if section is not None:

                values.append (line[tag.start(): tag.end ()][section.start () +1: section.end () -1])
            else:
                # TODO: better exception raising
                raise "section without name."


    active_template = Template.objects.Current ()
    for value in values:

        # TODO: be sure to make section name in lower (icase sensetive).
        layout, created = TemplateLayouts.objects.get_or_create (Template=active_template,\
                                                                 Section=value.lower ())

        
    return template_stream



def FillSections (stream):
    """
    Fill sections and depload tags.
    """
    # TODO: build a cach for this function 
    active_template = Template.objects.Current ()
    sections = TemplateLayouts.objects.filter (Template=active_template)
    depload = ""
    result = stream
    for section in sections:
        tmp_stream = ""
        contents = section.Contents.all ()
        for content in contents:
            tmp_stream = tmp_stream +  "{% %s %s %}\n" % \
                         (content.Name, " ".join (content.Params.split("&:&")))
            depload = depload + "{% load %s %}" % content.ModuleName
        result = result.replace ("{% section %s %}")


def ParseBase (baseaddress , basefile):
    try:
        # if cache file exists

        fd = open (safe_join (baseaddress, 'cache') , 'r')
        fdate = fd.readlines ()[0]
        fd.close ()
    except IOError:
        # if cache file does not exists
        sdate = modification_date (safe_join (baseaddress, basefile))
        fd = open (safe_join (baseaddress, basefile))
        stream = fd.read ()
        fd.close ()
        result = tmp_BaseParser (stream)
        fd = open (safe_join (baseaddress, 'cache') , 'w+')
        fd.write (sdate)
        fd.close ()
        return None
    
    
    sdate = modification_date (safe_join (baseaddress, basefile))
    res =  date_cmp (fdate, sdate)
    
    # TODO: handle the situation that fdate contain invalid date format
    
    if res == 0:
        return None
    # Handle the time mismatch 
    if res == 1 or res == 2:
        fd = open (safe_join (baseaddress, basefile))
        stream = fd.read ().decode(settings.FILE_CHARSET)
        fd.close ()
        result = tmp_BaseParser (stream)
        fd = open (safe_join (baseaddress, 'cache') , 'w+')
        fd.write (sdate)
        fd.close ()
        return result
