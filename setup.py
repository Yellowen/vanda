#!/usr/bin/env python
# -----------------------------------------------------------------------------
#    Vanda - A free platfrom for rapid web development
#    Copyright (C) 2012 Yellowen
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

from setuptools import setup, find_packages

setup(name='Vanda',
      version='2.0.0',
      description='Rapid web development platform based on Django framework',
      author='Sameer Rahmani',
      author_email='lxsameer@gnu.org',
      url='http://www.vandaproject.com/',
      download_url="http://www.vandaproject.com/downloads/",
      keywords="web development framework platform",
      license='GPL v3',
      packages=find_packages(),
      install_requires=['django', ],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Utilities',
          ]
)
