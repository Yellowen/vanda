# -----------------------------------------------------------------------------
#    Vanda Core - Vanda core utilities
#    Copyright (C) 2011 Sameer Rahmani <lxsameer@gnu.org>
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
import time
import logging


def log_this(func):
    """
    Logger decorator for debugging.
    """
    logger = logging.getLogger("debug")
    logger.info("Function: %s" % func.__name__)

    def new_func(*argc, **kwargs):
        """
        Function wrapper for decorator.
        """
        logger.debug("ARGC: %s" % str(argc))
        logger.debug("KWARGS: %s" % str(kwargs))
        b = time.time()
        result = func(*argc, **kwargs)
        a = time.time()
        logger.info("Run time: %s" % str(a - b))
        logger.debug("Result: %s" % str(result))
        return result

    return new_func
