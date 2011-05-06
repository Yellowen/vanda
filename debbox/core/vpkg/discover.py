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

import logging


class ApplicationDiscovery (object):
    """
    Discover the installed applications and the stuff about them like
    url patterns and settings attributes.
    """

    class InvalidBackend (Exception):
        """
        Unsupported backend passed to vpkg.
        """
        pass

    def load_backend(self, backend):
        """
        renturn the Backend class of specifyed backend.
        """
        pythonic_path = "backends.%s.Backend" % backend
        try:
            Backend = __import__(pythonic_path, globals(),
                                 locals(), [], -1)

            return Backend
        except ImportError:
            return None

    def __init__(self, **kwargs):

        # loading needed backend for vpkg
        if "backend" in kwargs:
            backend = self.load_backend(kwargs["backend"])
            if backend:
                self.backend = backend(**kwargs)
            else:
                raise self.InvalidBackend("Invalid backend '%s'" %
                                          kwargs["backend"])
        else:
            self.backend = self.load_backend("database")(**kwargs)

        if "logger" in kwargs:
            self.logging = kwargs["logger"]
        else:
            self.logging = logging

        self.urls = dict()
        self.urls_cache = dict()
        self.apps = None

    def installed_application(self):
        """
        Return the list of installed applications.
        """
        return self.backend.installed_application()

    def _apps_list(self):
        """
        create a list from discovered application
        Application interface.
        """
        apps = None
        result = list()
        if self.apps:
            apps = self.apps
        else:
            apps = self.installed_applications()

        for application in apps:
            try:
                # bapp is implementation of BaseApplication by package
                bpp_pypath = "%s.application" % application
                bapp = __import__(bpp_pypath,
                                  globals(),
                                  locals(), ["app"], -1)

                # application interface
                iapplication = bapp.app
                result.append([iapplication.priority, iapplication,
                               application])
            except ImportError:
                self.logger.debug("Can't import %s" % application)

        result.sort()
        return result

    def register_url(self, url, priority, elementnum):
        """
        register the given url into self.urls
        """
        current_url = None
        try:
            current_url = url[0].next()
        except StopIteration:
            # urls_list don't have any url element
            # TODO: generate a new url pattern for prev_url
            # or skip it
            self.logger.warning("Can't register url for %s" % \
                           self.urls_cache[str(priority)]["name"])
            return False

        if current_url in self.urls.keys():
            # url already registered
            prev_url = self.urls[current_url]

            # get the url list element that prev_urls belongs to
            prev_urls_list = self.urls_cache[str(prev_url[1])]["cache"][prev_url[2]]
            # looking to next urls element for alternative for prev_url
            self.register_url(prev_urls_list, prev_url[1], prev_url[2])
        self.urls[current_url] = [url[1], priority, elementnum]
        return True

    def _create_pattern(self):
        """
        create a pattern from self.urls.
        """
        from django.conf.urls.defaults import patterns

        tmplist = ['', ]
        for url in self.urls:
            action = self.urls[url][0]
            if not action:
                priority = self.urls[url][1]
                pypath = self.urls_cache[str(priority)]["path"]
                action = "%s.urls" % pypath
            tmplist.append((url, action))

        return patterns(*tmplist)

    def url_patterns(self):
        """
        produce a pattern object from discovered application IApplication
        implementation.
        """

        applications = self._apps_list()
        for application in applications:
            # get the application provided urls
            urls_list = application[1].url_patterns()
            priority = application[0]
            self.urls_cache[str(priority)] = {
                "cache": urls_list,
                "name": application[1].__class__.__name__,
                "path": application[2],
                }

            element = 0
            for url in urls_list:
                self.register_url(url, priority, element)
                element += 1

        return self._create_pattern()
