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
import os
import logging

from django.conf import settings


class LoggerBase (object):
    """
    Debbox Main logger class.
    """

    def _init__(self, **kwarg):

        logparam = {}
        handlerparam = {}
        try: logparam['level'] = settings.LOG_LEVEL
        except AttributeError: pass

        try: logparam['format'] = settings.LOG_FORMAT
        except AttributeError: pass

        try: logparam['datefmt'] = settings.LOG_DATE_FORMAT
        except AttributeError: pass

        try: handlerparam['maxBytes'] = settings.LOG_MAX_BYTES
        except AttributeError: pass

        try: handlerparam['backupCount'] = settings.LOG_BACKUP_COUNT
        except AttributeError: pass

        LOG_FILENAME = "/var/log/debbox"
        try: LOG_FILENAME = settings.LOG_FILENAME
        except AttributeError: pass

        logparam.update(kwarg)
        self.logger = logging.basicConfig(**logparam)

        self.logger = logging.getLogger("TODO")
        handler = logging.handlers.RotatingFileHandler(
              LOG_FILENAME, **handlerparam)
        self.logger.addHandler(handler)
        self.logger("asdasdasdasdadasdqweqweqweq")

    def info(self, s):
        return self.logger.info(s)

    def debug(self, s):
        return self.logger.debug(s)

logger = LoggerBase()
