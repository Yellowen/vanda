# -----------------------------------------------------------------------------
#    Vanda news - News application for vanda platform
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

from vpkg.base import BaseApplication
from vpkg import vpkg


class News(BaseApplication):
    """
    Implementation of BaseApplication interface for news application.
    this class allow vpkg to discover it.
    """

    application_name = "News"
    priority = 50
    urls = [
        (['^news/', '^news_page/'], None),
        ]

    settings = {
        "NEWS_LIMIT": 10,
        }

vpkg.register(News)
