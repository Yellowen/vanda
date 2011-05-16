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

from debbox.core.logging import logger


def load_dashboard_instance(application):
    """
    Load the Dashboard class of the given application and return an instance.
    application should be a pythonic path to a application.

    This function will look for a dashboard module inside the application and
    a Dashboard class inside the module.
    """
    dashboard_path = "%s.dashboard" % application
    try:
        __import__(dashboard_path, globals(), locals(),
                   ["dashboard", ], -1)

    except ImportError, e:
        logger.debug("Can not import the dashboard module of '%s'" %
                     application)
        logger.debug(str(e))
        return None
