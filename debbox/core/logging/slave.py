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


class SlaveLogger (object):
    """
    Debbox Slave process logger.
    """

    def __new__(cls):
        from debbox.core.communication import MasterClient
        cant_connect = None
        client = MasterClient()
        try:
            client.connect()
            result = client.command("get_config", config=("Log", "folder"))
            logfolder = result.result
            client.disconnect()
            LOG_FILENAME = "/".join((logfolder.rstrip("/"), "webserver.log"))
        except client.CantConnectToSocket:
            cant_connect = True

        logparam = {}
        handlerparam = {}
        logparam['level'] = conf.LOG_LEVEL
        logparam['format'] = conf.LOG_FORMAT
        logparam['datefmt'] = conf.LOG_DATE_FORMAT
        handlerparam['maxBytes'] = conf.LOG_MAX_BYTES
        handlerparam['backupCount'] = conf.LOG_BACKUP_COUNT
        logging.basicConfig(**logparam)
        logger = logging.getLogger("TODO")
        if not cant_connect:
            handler = RotatingFileHandler(
                LOG_FILENAME, **handlerparam)

            formatter = logging.Formatter(logparam['format'])
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger

