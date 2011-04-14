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


# unique place for creating debbox socket
SOCKFILE = "/var/run/debbox.sock"

# logger configuration

# level values
# logger.DEBUG
# logger.WARNING
#  . . .
LOG_LEVEL = 1

LOG_FORMAT = '[%(asctime)s] [%(filename)s-%(funcName)s],' + \
            ' line:%(lineno)d-> %(levelname)-8s : "%(message)s"'

LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
LOG_MAX_BYTES = 2 * 1024 * 1024  # 2Mb
LOG_BACKUP_COUNT = 5
