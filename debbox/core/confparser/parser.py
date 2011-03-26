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

from django.conf import settings

from core.log import logger


class BaseParser (object):
    """
    Base class for all type of config parser.
    """

    def __init__(self, inputfile, cached=True):
        self._file = inputfile
        self.cached = cached
        self._dict = {}
        # TODO: does caching is required?
        if os.path.exists(self._file) and cached:
            self._buf = self._read()
            # parse the string to config
            self.__config__()
        else:
            self._buf = None
        self.load()

    def _read(self):
        return file(self._file).read()

    def load(self):
        pass

    def get_option(self, option_name, default_value=None):
        if option_name in self._dict.keys():
            return self._dict[option_name]
        else:
            return default_value

    def __getitem__(self, key):
        if key in self._dict:
            return self._dict[key]
        else:
            raise self.KeyError(key)

    def set_option(self, option_name, option_value):
        self._dict[option_name] = option_value

    def __setitem__(self, key, value):
        self._dict[key] = value

    def commit(self):
        """
        write configuration into file.
        """
        if self._buf:
            try:
                fd = open(self._file, "w")
                fd.write(self.__unicode__)
            except Exception, e:
                logger.warn("%s failed to commit configurations. Error: %s" % \
                            (self.__name__, e))
                raise

    # TODO: need extra consideration
    @classmethod
    def is_suitable(cls, buf):
        """
        check whether current class is suite for parsing  buf conf string
        or not. if current class is a suitable parser then return class else
        return None
        """
        pass

    def __config__(self):
        """
        This method parse the self._buf string to a dictionary. and should
        override by any inherited class.
        """
        pass

    def __unicode__(self):
        """
        BaseParser use this standard method to convert self._buf to
        real confiuration string. This method should override by user.
        """
        pass

    class KeyError (Exception):
        pass


class Parser (object):
    """
    Config parser class for debbox. this class will load config drivers
    and finde suitable driver for current configuration file.
    """

    def __init__(self, conf_file, driver=None):
        """
        conf_file is the path of target configuration.
        if conf_file does not exists driver parameter should
        specify the config parser driver for building new
        configuration file.
        """
        self.driver = None
        if os.path.exists(conf_file):
            self._file = conf_file
            from core.confparser.parsers import drivers

            self._drivers = drivers
            self._init_external_drivers()
            self._buf = self._read_configuration()
            self.find_suitable_driver()

        else:
            if not driver:
                raise self.DoesNotExist()
            else:
                self.driver = driver
                try:
                    fd = open(conf_file, 'w')
                    fd.close()
                except:
                    raise

                self._file = conf_file
                self.driver = driver(self._file)

    def _init_external_drivers(self):
        """
        Update the _driver_list with external drivers that may defines in
        settings.py by CONF_PARSERS option
        """
        try:
            self._drivers.extend(settings.CONF_PARSERS)
        except AttributeError:
            pass

    def _read_configuration(self):
        return file(self._file).read()

    def find_suitable_driver(self):
        """
        try to load first match driver.
        """
        for driver in self._drivers:
            # TODO: need a good exception handling.
            path = ".".join(driver.split(".")[:-1])
            name = driver.split(".")[-1]
            cls = __import__(path, globals(),
                             locals(),
                             [name, ],
                             - 1)

            logger.debug("cls type: %s", str(type(cls)))
            drv = cls.__dict__[name].is_suitable(self._buf)
            if drv:
                self.driver = drv(self._file)
                break

        if not self.driver:
            raise self.TypeNotSupported()

        logger.debug("suitable confparser driver selected: %s" % self.driver)

    def __getitem__(self, key):
        """
        return the value of given config_name
        valie <= Parser_instanse[key]
        """
        return self.driver[key]

    def __setitem__(self, key, value):
        """
        set the value of given key name to value.
        """
        self.driver[key] = value

    def commit(self):
        """
        write current configuration to config file.
        """
        self.driver.commit()

    class DoesNotExist (Exception):
        pass

    class TypeNotSupported (Exception):
        pass
