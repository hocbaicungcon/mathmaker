# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2015 Nicolas Hainaux <nico_h@users.sourceforge.net>

# This file is part of Mathmaker.

# Mathmaker is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.

# Mathmaker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Mathmaker; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import os, sys
import configparser

from lib.common import software

class default_object(object):
    def __init__(self):
        self.LANGUAGE = CONFIG["LOCALES"]["LANGUAGE"]
        self.ENCODING = CONFIG["LOCALES"]["ENCODING"]
        self.NUMBER_OF_QUESTIONS = 6
        self.MONOMIAL_LETTER = 'x'
        self.EQUATION_NAME = 'E'

def init():
    global rootdir
    global localedir
    global configfile_name
    global CONFIG
    global language
    global default

    __process_name = os.path.basename(sys.argv[0])
    __abspath = os.path.abspath(sys.argv[0])
    __l1 = len(__process_name)
    __l2 = len(__abspath)
    rootdir = __abspath[:__l2-__l1]
    localedir = rootdir + "locale/"

    configfile_name = rootdir + software.NAME + '.cfg'

    CONFIG = configparser.ConfigParser()
    CONFIG.read(configfile_name)

    default = default_object()

    language = None
