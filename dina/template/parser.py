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


class TemplateSyntaxError (Exception):
    def __init__ (self, line , char):
        super(TemplateSyntaxError, self).__init__ ("Invalide syntax: '%s' char: %s." % (line , char))



class Section (object):

    def __init__ (self,  **params):
        self.Name = params["name"]
        self.Width = params["width"]
        self.Height = params["height"]
        self.params = params["parameters"]



class HTMLParser (object):
    """
    this class provide a simple template tag parser that allow dina
    to fill the specific position of a template.
    """


    def __init__ (self, template_stream , openmark = None , closemark= "%}"):
        self.template = template_stream.split ("\n")
        self.OPENMARK = openmark
        self.CLOSEMARK = closemark

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
    
