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

from django.http import HttpResponseRedirect

from models import Setting


class check_auth (object):
    """
    Check for allowing anonymous comment in settings if its set to
    False and user did not authenticated it redirect to '/login/'
    """
    
    def __init__ (self, func, redirect='/login/'):
        
        self.func = func
        self.redirect = redirect

        
    def __call__ (self, request, *args, **kwargs):
        
        setting = Setting.configs ()
        
        if not (setting.allow_anonymous_comment and request.user.is_authenticated()):
            return HttpResponseRedirect (self.redirect)
        return self.func (request, *args, **kwargs)

