# -----------------------------------------------------------------------------
#    Vanda multilang
#    Copyright (C) 2012  Sameer Rahmani <lxsameer@gnu.org>
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
import datetime

from django.utils.translation import activate
from django.core.urlresolvers import resolve
from django.conf import settings
from django.http import Http404


def set_cookie(response, key, value, days_expire=7):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  # One year
    else:
        max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.strftime(
        datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
        "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key,
                        value,
                        max_age=max_age,
                        expires=expires,
                        domain=settings.SESSION_COOKIE_DOMAIN,
                        secure=settings.SESSION_COOKIE_SECURE or None)


def dispatch_url(request, lang=None):
    """
    Dispatch the urls again against the LEAF_URLCONF.
    """
    _lang = lang
    print ">> ", lang
    need_cookie = True

    if lang:
        request.path = request.path[len(lang) + 1:]
        print "111"
    else:
        if settings.LANGUAGE_COOKIE_NAME in request.COOKIES:
            _lang = request.COOKIES[settings.LANGUAGE_COOKIE_NAME]
            request.session['django_language'] = _lang
            need_cookie = False
            print "222"
        else:
            if "django_language" in request.session:
                _lang = request.session["django_language"]
                print "333"
            else:
                _lang = settings.LANGUAGES[0][0]
                print "444"

    try:
        view = resolve(request.path, settings.LEAF_URLCONF)
        request.session['django_language'] = _lang
        activate(_lang)
        setattr(settings, "LANGUAGE_CODE", _lang)
        print "<<<< ", request.path, _lang
        response = view.func(request, *view.args, **view.kwargs)
        if need_cookie:

            set_cookie(response, settings.LANGUAGE_COOKIE_NAME, _lang)

        return response

    except Http404:
        raise
