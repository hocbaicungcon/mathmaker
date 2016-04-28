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
import logging, logging.config
import yaml
from shutil import copyfile

from lib.common import software

class default_object(object):
    def __init__(self):
        self.NUMBER_OF_QUESTIONS = 6
        self.MONOMIAL_LETTER = 'x'
        self.EQUATION_NAME = 'E'

class config_object(object):
    def __init__(self):
        self.LANGUAGE = CONFIG["LOCALES"]["LANGUAGE"]
        self.ENCODING = CONFIG["LOCALES"]["ENCODING"]
        self.MARKUP = CONFIG['MARKUP']['USE']

class path_object(object):
    def __init__(self):
        self.db = datadir + "mathmaker.db"
        self.db_dist = datadir + "mathmaker.db-dist"
        if not os.path.isfile(self.db)\
            or os.path.getmtime(self.db) < os.path.getmtime(self.db_dist):
            copyfile(self.db_dist, self.db)

def init():
    global rootdir, localedir, libdir, datadir
    global configfile_name, CONFIG, config
    global default, path
    global mainlogger
    global language

    __process_name = os.path.basename(sys.argv[0])
    __abspath = os.path.abspath(sys.argv[0])
    __l1 = len(__process_name)
    __l2 = len(__abspath)
    rootdir = __abspath[:__l2-__l1]
    localedir = rootdir + "locale/"
    libdir = rootdir + "lib/"
    datadir = rootdir + "data/"

    configfile_name = rootdir + software.NAME + '.cfg'
    CONFIG = configparser.ConfigParser()
    CONFIG.read(configfile_name)
    config = config_object()

    default = default_object()
    path = path_object()

    with open(libdir + "logging.yml") as f:
        logging.config.dictConfig(yaml.load(f))
    mainlogger = logging.getLogger("__main__")

    language = None
