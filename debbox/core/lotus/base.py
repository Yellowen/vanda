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

from twisted.internet import reactor
from twisted.web import static, server
from twisted.web.resource import Resource
from twisted.web.wsgi import WSGIResource
from twisted.python.threadpool import ThreadPool


class Root(Resource):
    """
    Root resource that combines the two sites/entry points
    """

    WSGI = None

    def getChild(self, child, request):
        request.prepath.pop()
        request.postpath.insert(0, child)
        return self.WSGI

    def render(self, request):
        """
        Delegate to the WSGI resource
        """
        return self.WSGI.render(request)


class LotusServer(object):
    """
    Debbox Web Server. This class is based one twisted web.
    """

    def __init__(self, WSGI_app):
        self.pool = ThreadPool()
        self.pool.start()
        self.app = WSGI_app

        reactor.addSystemEventTrigger('after',
                                      'shutdown',
                                      self.pool.stop)

        self.wsgi_resource = WSGIResource(reactor,
                                          self.pool,
                                          self.app)
        self.wsgi_resource.putChild("statics",
                                      static.File("/home/lxsameer/src/www"))

    def start(self):
        reactor.listenTCP(80, server.Site(self.wsgi_resource))
        reactor.run()
