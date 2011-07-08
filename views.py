# -----------------------------------------------------------------------------
#    Vanda - Web development platform
#    Copyright (C) 2011 Some Hackers In Town
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
# -----------------------------------------------------------------------------

from django.shortcuts import render_to_response as rr
from django.template import RequestContext
from django.contrib.auth.models import User

from forms import PreRegistrationForm


def pre_register(request):
    if request.method == "POST":
        form = PreRegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            #user = User.objects.filter(email=data["email"])
            #user, created = User.objects.get_or_create(username=data["username"],
            #                                           email.
        else:
            return rr("pre_registeration.html",
                      {"form": form},
                      context_instance=RequestContext(request))
    else:
        form = PreRegistrationForm()
        return rr("pre_registeration.html",
                  {"form": form},
                  context_instance=RequestContext(request))
