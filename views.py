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
from django.db import transaction
from django.http import Http404
from django.utils.translation import ugettext as _

from forms import PreRegistrationForm
from mail import VerificationMail
from models import Verification


def pre_register(request):
    """
    First step of registeration process. In this step we process
    just username and email address and send a verification mail.
    """
    if request.method == "POST":
        form = PreRegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # collect queries in a single transaction
            with transaction.commit_on_success():
                email = User.objects.filter(email=data["email"])
                user = User.objects.filter(username=data["username"])

            if email or user:
                # returning suitable error if email or user already registered 
                if email:
                    form.errors["email"] = (_("This Email already registered."),)
                if user:
                    form.errors["usernmae"] = (_("This Username already registered."),)
                return rr("pre_registeration.html",
                      {"form": form},
                      context_instance=RequestContext(request))

            else:
                # Create a user and send the verification mail
                user =  User(username=data["username"], email=data["email"])
                user.save()

                # create verification code and save it in DB
                verification_code = Verification(user=user)
                code = verification_code.create_verification_code()

                vmail = VerificationMail(user, code, request.META["HTTP_HOST"])
                vmail.send()
        else:
            return rr("pre_registeration.html",
                      {"form": form},
                      context_instance=RequestContext(request))
    else:
        form = PreRegistrationForm()
        return rr("pre_registeration.html",
                  {"form": form},
                  context_instance=RequestContext(request))


def ajax_js(request):
    url = request.GET.get("validator", None)
    if url:
        return rr("validator.js", {"url": url})
    else:
        raise Http404()


def verificate_email(request, code):
    """
    Get the verification code and verify the user mail.
    """
    raise Http404()
