# -----------------------------------------------------------------------------
#    VPKG - Vanda Package manager
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

from ConfigParser import NoSectionError

from debbox.core.communication import MasterClient
from debbox.core.logging.instance import logger

from discover import ApplicationDiscovery


class DebboxApplicationDiscovery (ApplicationDiscovery):
    """
    Discover the installed applications and the stuff about them like
    url patterns and settings attributes.
    """

    class InvalidBackend (Exception):
        """
        Unsupported backend passed to vpkg.
        """
        pass

    def installed_applications(self):
        """
        Discover the current installed app and return the list of them.
        """
        if self.backend != "config":
            raise self.InvalidBackend()

        # Request the applications value from master process
        client = MasterClient()
        client.connect(True)
        try:
            result = client.command(command="get_config",
                                    config=["APP", "applications", [], ])
        except NoSectionError:
            logger.critical("There is no [APP] section in configuration file.")
            client.command(command="kill")

        except client.UnpicklableException:
            logger.warning("There is applications attribute in configuration file.")

        client.disconnect()
