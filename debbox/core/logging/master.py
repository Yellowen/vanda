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

import logging
from logging.handlers import RotatingFileHandler

from debbox.core import conf


class MasterLogger (object):
    """
    Debbox Master Process Logger.
    """

    def __new__(cls, config=None, logfile=None, debug=False):

        logparam = {}
        handlerparam = {}
        format_ = '[%(asctime)s] [%(filename)s-%(funcName)s],' + \
            ' line:%(lineno)d-> %(levelname)-8s : "%(message)s"'

        formatter = logging.Formatter(format_)

        if config:
            logparam['level'] = int(config.get("Log", "level"))
            logparam['format'] = format_
            logparam['datefmt'] = config.get("Log", "date_format")
            handlerparam['maxBytes'] = int(config.get("Log", "max_size"))
            handlerparam['backupCount'] = int(config.get("Log", "backups"))

        if logfile:
            LOG_FILENAME = logfile
        logging.basicConfig(**logparam)
        logger = logging.getLogger("Master")
        handler = RotatingFileHandler(
            LOG_FILENAME, **handlerparam)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
