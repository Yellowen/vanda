from django.shortcuts import render_to_response as rr
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.conf import settings
from django.utils.translation import ugettext as _

from forms import LoginForm
from debbox.core.logging.instance import logger


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
