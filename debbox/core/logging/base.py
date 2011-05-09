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
from ConfigParser import NoSectionError

from debbox.core import conf


def setup_logger(config=None, logfile=None, debug=False):
    """
    Setup the Master channel of Debbox logger.
    """
    logparam = {}
    handlerparam = {}
    formatter = logging.Formatter(conf.LOG_FORMAT)
    logparam['format'] = conf.LOG_FORMAT
    logparam['level'] = conf.LOG_LEVEL
    logparam['datefmt'] = conf.LOG_DATE_FORMAT
    handlerparam['maxBytes'] = conf.LOG_MAX_BYTES
    handlerparam['backupCount'] = conf.LOG_BACKUP_COUNT
    if config:
        try:
            logparam['level'] = int(config.get("Log", "level"))
            logparam['datefmt'] = config.get("Log", "date_format")
            handlerparam['maxBytes'] = int(config.get("Log", "max_size"))
            handlerparam['backupCount'] = int(config.get("Log", "backups"))
        except NoSectionError:
            print "Malform config file. 'Log' section is missing."
            print "Skipping."

    logging.basicConfig(**logparam)
    logger = logging.getLogger("Master")

    if logfile:
        LOG_FILENAME = logfile
        handler = RotatingFileHandler(
        LOG_FILENAME, **handlerparam)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    else:
        pass
    return logger
