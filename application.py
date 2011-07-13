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
from django.core.urlresolvers import reverse

from vpkg.base import BaseApplication
from vpkg import vpkg


class Authentication(BaseApplication):
    """
    Implementation of BaseApplication interface for auth application.
    this class allow vpkg to discover it.
    """

    # You Should add some veriables to settings.py
    # SMTP settings, look at the sending mail section of django docs.
    # SMTP_FROM the mail address that you want to mail sent by.
    # WEBSITE_TITLE the title of current site.
    # SUPPORT_MAIL the email address of support group

    application_name = "auth"
    priority = 10
    urls = [
        (['^auth/', '^account/'], None),
        ]

    # replace the absolute and static urls with dynamic ones
    settings = {
        "LOGIN_URL": "/auth/login/",
        "AUTH_PROFILE_MODULE": "auth.profile",
        "LOGIN_REDIRECT_URL": "/auth/profile/",
        "LOGOUT_URL": "/auth/logout/",
        }
vpkg.register(Authentication)
