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

import PAM

from django.contrib.auth.models import User
from django.conf import settings

from core.log import logger


class UserNameNotProvided (Exception):
    pass


class PasswordNotProvided (Exception):
    pass


class PAMAuthentication (object):
    """
    PAM authentication backend for django.
    """

    def __init__(self):
        self._pam = PAM.pam()
        self._service = settings.PAM_SERVICE
        self._pam.start(self._service)

    def get_user(self, user_id):
        # TODO: get_user should return user corresponded to current
        # authentication method not passwd only
        passwd = file("/etc/passwd").readlines()
        username = ""
        for line in passwd:
            fields = line.split(":")
            if fields[2] == int(user_id):
                username = fields[0]
        if username:
            try:
                user = User.objects.get(username=username())
                return user
            except User.DoesNotExist:
                # CHECK: should this method return none for invalid user
                return None

    def authenticate(self, **kwarg):
        if "username" in kwarg:
            self.username = kwarg["username"]
        else:
            raise UserNameNotProvided()

        if "password" in kwarg:
            self.password = kwarg["password"]
        else:
            raise PasswordNotProvided()
        self._pam.start("passwd")

        self._pam.set_item(PAM.PAM_USER, self.username)
        self._pam.set_item(PAM.PAM_CONV,
                           lambda auth, query, ud: [(self.password,
                                                     0)])

        try:
            self._pam.authenticate()

            try:
                user = User.objects.get(username=self.username)
            except User.DoesNotExist:
                user = User(username=self.username, password=self.password)
                # TODO: pam backend should check for a list of admin users
                if self.username == "root":
                    user.is_staff = True
                    user.is_superuser = True
            user.save()
            return user

        except PAM.error, response:
            logger.warn("Login attempt failed. username: '%s' password: '%s'" % \
                        (self.username, self.password))
            return None
