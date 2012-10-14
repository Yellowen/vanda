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


from django.conf import settings
from django.contrib.auth.models import User

from debbox.core.logging import logger
from debbox.core.communication import MasterClient


class PAMAuthentication (object):
    """
    PAM authentication backend for django.
    """

    def authenticate(self, username=None, password=None):
        service = settings.PAM_SERVICE

        # establish connection to master server through MasterClient
        # to send a authentication command.
        try:
            mclient = MasterClient()
        except (MasterClient.CantFindConfigFile, IOError):
            # TODO: show a good error page to user and alert him
            # about the error
            raise

        try:
            mclient.connect()
        except MasterClient.CantConnectToSocket:
            # TODO: show a good error page to user and alert him
            # about the error
            raise

        result = mclient.command("authenticate",
                                 username=username,
                                 password=password,
                                 service=service)
        if result.status == 0:
            if result.result:
                try:
                    user = User.objects.get(username=username)
                except:
                    user = User(username=username, password='None')

                    # Setting up root user
                    root_user = getattr(settings, 'PAM_SUPERUSER', "root")
                    if user.username == root_user:
                        user.is_superuser = True
                        user.is_staff = True

                    user.save()
                logger.debug("Loging '%s' user in." % username)
                return user

        logger.warn("Login failed with username: %s password: %s" % \
                    (username, password))
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
