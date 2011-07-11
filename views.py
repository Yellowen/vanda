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
from django.http import (Http404, HttpResponseForbidden,
                         HttpResponseRedirect)
from django.utils.translation import ugettext as _
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from forms import PreRegistrationForm, PostRegistrationForm
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
                    form.errors["email"] = (
                        _("This Email already registered."), )
                if user:
                    form.errors["usernmae"] = (
                        _("This Username already registered."), )
                return rr("pre_registeration.html",
                      {"form": form},
                      context_instance=RequestContext(request))

            else:
                # Create a user and send the verification mail
                user = User(username=data["username"], email=data["email"],
                                    is_active=False)
                user.save()

                # create verification code and save it in DB
                verification_code = Verification(user=user)
                code = verification_code.create_verification_code()

                vmail = VerificationMail(user, code, request.META["HTTP_HOST"])
                vmail.send()
                return rr("verification_sent.html")

        else:
            return rr("pre_registeration.html",
                      {"form": form},
                      context_instance=RequestContext(request))
    else:
        form = PreRegistrationForm()
        return rr("pre_registeration.html",
                  {"form": form},
                  context_instance=RequestContext(request))


def post_register(request):
    """
    Complete the registeration by asking user to fill extra information.
    """

    user = None
    if "user" in request.session:
        user = request.session["user"]
    else:
        return HttpResponseForbidden()

    if request.method == "POST":
        form = PostRegistrationForm(request.POST)
        if form.is_valid():
            try:
                form.save(user)
            except form.PasswordError, e:
                form.errors["password1"] = unicode(e)
                form.errors["password2"] = unicode(e)
                return rr("post_registeration.html",
                          {"form": form},
                          context_instance=RequestContext(request))

            user = authenticate(username=user.username,
                                password=form.cleaned_data["password1"])
            login(request, user)
            return HttpResponseRedirect(reverse("auth.views.profile",
                                                args=[]))
        else:
            return rr("post_registeration.html",
                          {"form": form},
                          context_instance=RequestContext(request))

    else:
        form = PostRegistrationForm()
        return rr("post_registeration.html",
                  {"form": form},
                  context_instance=RequestContext(request))


@login_required
def profile(request):
    """
    User profile main view.
    """
    pass


def ajax_js(request):
    """
    Return a suitable javascript code for given url.
    """
    url = request.GET.get("validator", None)
    if url:
        return rr("validator.js", {"url": url})
    else:
        raise Http404()


def verificate_email(request, code):
    """
    Get the verification code and verify the user mail.
    """
    # Look for given verification code
    try:
        verification = Verification.objects.get(code=code)

    except Verification.DoesNotExist:
        # always riase a 404 status code for invalid code
        raise Http404()

    # if verification code sent ins last 48 hours
    if verification.is_valid():
        # Activating user
        user = verification.user
        user.is_active = True
        user.save()

        request.session["user"] = user
        verification.delete()

        form = PostRegistrationForm()
        return rr("post_registeration.html",
                  {"form": form},
                  context_instance=RequestContext(request))
    else:
        # If code expired.
        verification.delete()
        raise Http404()
