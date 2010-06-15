#! /bin/bash
# ---------------------------------------------------------------------------------
#    Jin programmer suite
#    Copyright (C) 2010  Sameer Rahmani <lxsameer@gnu.org>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# ---------------------------------------------------------------------------------


param=$1
commands='\n
todo  \tList all TODOs that commented in the source code.\n
sourceclean \tDelete all the *.pyc and *~ files.\n
\n'

if [ -z "$1" ]; then
    
    echo "Please enter a command as first parameter."
    echo "availabe commands:"
    echo -e $commands
    exit 0
fi      

if [ "$param" = "todo" ]; then 
    grep "# TODO" ./ -Rn
    exit 0
fi


if [ "$param" = "sourceclean" ]; then 
    rm -v `find ./ -iname "*.pyc"`
        rm -v `find ./ -iname "*~"`
    exit 0
fi
    


echo "Error: jin command '$param' not found ! "
exit 1
