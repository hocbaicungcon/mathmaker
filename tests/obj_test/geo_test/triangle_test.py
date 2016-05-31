# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2014 Nicolas Hainaux <nico_h@users.sourceforge.net>

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

import os
import sys
#import locale

#from settings import config

from lib.core import *
from lib.core.base_calculus import *
from lib.core.base_geometry import *
from lib.core.geometry import *

from maintenance.autotest import common

#try:
#   locale.setlocale(locale.LC_ALL, config.LANGUAGE + '.' + config.ENCODING)
#except:
#    locale.setlocale(locale.LC_ALL, '')

check = common.check


def action():
    if common.verbose:
        os.write(common.output, bytes("--- [GEO] TRIANGLE \n", 'utf-8'))

    # Don't forget to uncomment the convenient lines above if a test
    # requires to use the locale module.

    # 1
    t1 = Triangle((("Z", "E", "P"),
                   {'side0':4, 'angle1':64, 'side1':5}
                  ),
                  rotate_around_isobarycenter=115
                 )
    t1.side[0].label = Value(4, unit='cm')
    t1.side[1].label = Value(5, unit='cm')
    t1.side[2].label = Value(4.84, unit='cm')
    t1.angle[0].label = Value('?')
    t1.angle[1].label = Value(64, unit='\\textdegree')
    t1.angle[2].label = Value(35, unit='\\textdegree')
    t1.angle[0].mark = 'simple'
    t1.angle[1].mark = 'double'
    t1.angle[2].mark = 'dotted'


    check(t1.into_euk(),
          ["box -1.32, -0.48, 4.71, 4.6"\
           "Z = point(4.11, 0.37)"\
           "E = point(2.42, 4)"\
           "P = point(-0.72, 0.12)"\
           "draw"\
           "  (Z.E.P)"\
           "  $\\rotatebox{-65}{4~cm}$ Z 115 - 7.5 deg 6.5"\
           "  $\\rotatebox{51}{5~cm}$ E 231 - 6.5 deg 8"\
           "  $\\rotatebox{3}{4,84~cm}$ P 3 - 6.7 deg 7.8"\
           "  $\\rotatebox{-31.2}{?}$ Z 148.8 deg 2.7"\
           "  $\\rotatebox{82.9}{64\\textdegree}$ E 262.9 deg 2.7"\
           "  $\\rotatebox{27}{35\\textdegree}$ P 27 deg 2.7"\
           "end"\
           "label"\
           "  E, Z, P simple"\
           "  P, E, Z double"\
           "  Z, P, E dotted"\
           "  Z 328.8 deg"\
           "  E 82.9 deg"\
           "  P 207 deg"\
           "end"])