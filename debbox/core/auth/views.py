# -----------------------------------------------------------------------------
#    Debbox - Modern administration panel for Debian GNU/Linux
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
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.conf import settings
from django.utils.translation import ugettext as _

from forms import LoginForm
from debbox.core.logging import logger


def Login(request):
    """
    login view.
    """
    if request.user.is_authenticated():
        logger.debug("User is authenticated, redirecting to /")
        return HttpResponseRedirect("/")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            logger.debug("Login form is valid.")
            user = authenticate(username=form.cleaned_data["username"],
                                password=form.cleaned_data["password"])
            logger.debug("USER: %s", user)
            if user:
                if user.is_active:
                    logger.debug("Try to loging in the user")
                    result = login(request, user)
                    logger.debug("login return with %s", result)
                    return HttpResponseRedirect("/")

                else:
                    msg = _("Your account is disable.")
                    return rr("auth/login.html",
                              {"form": form,
                               "msg": msg},
                              context_instance=RequestContext(request))
            else:
                msg = _("Invalid login informations.")
                return rr("auth/login.html",
                          {"form": form,
                           "msg": msg},
                          context_instance=RequestContext(request))

        # Form is not valid
        # ISSUE : Show messages for logging to user
        return rr("auth/login.html",
                  {"form": form},
                  context_instance=RequestContext(request))
    else:
        form = LoginForm()
        return rr("auth/login.html",
                  {"form": form},
                  context_instance=RequestContext(request))


def Logout(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)

