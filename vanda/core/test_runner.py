# -----------------------------------------------------------------------------
#    Vanda Core - Vanda core utilities
#    Copyright (C) 2011-2013 Sameer Rahmani <lxsameer@gnu.org>
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

from django.test.simple import DjangoTestSuiteRunner
from django.conf import settings


class ExcludeAppsTestSuiteRunner(DjangoTestSuiteRunner):
    """
    Override the default django 'test' command. It now supports application
    exclusion.
    """

    def run_tests(self, test_labels,
                  extra_tests=None,
                  **kwargs):
        if not test_labels:
            # No appnames specified on the command line, so we run all
            # tests, but remove those which we know are troublesome.
            TEST_EXCLUDE_APPS = getattr(settings, "TEST_EXCLUDE_APPS", [])

            test_labels = [app for app in settings.INSTALLED_APPS
                            if not app in TEST_EXCLUDE_APPS
                            and not app.startswith('django.')]

        return super(ExcludeAppsTestSuiteRunner, self).run_tests(
                                      test_labels, extra_tests, **kwargs)
