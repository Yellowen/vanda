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

from optparse import make_option

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--cache',
                    action='store_true',
                    dest='delete',
                    default=False,
                    help='Delete poll instead of closing it'),
        )
    help = "Command line interface to Vanda package manager (VPKG)."

    # Validation is called explicitly each time the server is reloaded.
    requires_model_validation = False
    can_import_settings = False

    def handle(self, *args, **options):
        print ">>> ", args
        print "<<< ", options
