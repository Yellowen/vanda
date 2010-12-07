b#! /usr/bin/env python
# -----------------------------------------------------------------------------
#    Dina Project
#    Copyright (C) 2010  Dina Project Community
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
import json
from libdpm.utils import safe_join


class Control (object):
    """
    Control class is a interface to dina/control file.
    """

    def __init__(self, cwd, new=None):
        self.path = safe_join(cwd, "control")
        if not new:
            if self._exists():
                self._control = json.loads(file(self.path).read())
            else:
                raise self.DoesNotExist()
        else:
            self._control = {
                "Source": "",
                "Package": "",
                "Version": "",
                "Section": "",
                "Priority": "",
                "Uploaders": "",
                "Maintainer": "",
                "Home": "",
                "Vcs-home": "",
                "Vcs-browse": "",
                "Depends": "",
                "Build-Depends": "",
                "Recommends": "",
                "Suggest": "",
                "Description": {"Short": "",
                                "Extra": "",
                                }
                }
            self._new = new

    def _exists(self):
        if os.path.exists(self.path):
            return True
        else:
            return False

    def validate(self):
        """
        validate current data
        """
        # TODO: build a complete validation method
        return True
        if "Package" not in self._control.keys():
            raise self.DoesNotValid("'Package' field was not found.")
        else:
            pass

        if "Maintainer" not in self._control.keys():
            raise self.DoesNotValid("'Maintainer' field was not found.")

        if "Priority" not in self._control.keys():
            raise self.DoesNotValid("'Priority' field was not found.")

        if "Section" not in self._control.keys():
            raise self.DoesNotValid("'Section' field was not found.")

    def flush(self):
        """
        write data to disk.
        """
        flag = None
        exi = self._exists()
        if exi and not self._new:
            flag = "a+"
        elif exi and self._new:
            flag = "w+"
        elif not exi and self._new:
            flag = "w+"
        elif not exi and not self._new:
            raise self.DoesNotExist()
        fd = open(self.path, flag)
        self.validate()
        fd.write(json.dumps(self._control).replace(",", ",\n"))
        fd.close()
        return True

    class DoesNotValid (Exception):
        pass

    class DoesNotExist (Exception):
        pass
