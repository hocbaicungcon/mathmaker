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

import pytest
import decimal

from lib.core.root_calculus import Value
from lib.core.base_geometry import Point
from lib.core.geometry import Polygon
from tools import wrap_nb


def test_p1_into_euk():
    """Check Polygon's generated euk file."""
    p1 = Polygon([Point(["A", (0.5, 0.5)]),
                  Point(["B", (3, 1)]),
                  Point(["C", (3.2, 4)]),
                  Point(["D", (0.8, 3)])
                  ])
    p1.side[0].label = Value(4, unit='cm')
    p1.side[1].label = Value(3, unit='cm')
    p1.side[2].label = Value(2, unit='cm')
    p1.side[3].label = Value(6.5, unit='cm')
    p1.angle[0].label = Value(64, unit="\\textdegree")
    p1.angle[1].label = Value(128, unit="\\textdegree")
    p1.angle[2].label = Value(32, unit="\\textdegree")
    p1.angle[3].label = Value(256, unit="\\textdegree")
    p1.angle[0].mark = 'simple'
    p1.angle[1].mark = 'simple'
    p1.angle[2].mark = 'simple'
    p1.angle[3].mark = 'simple'
    assert p1.into_euk() == \
    'box -0.1, -0.1, 3.8, 4.6\n\n'\
    'A = point(0.5, 0.5)\n'\
    'B = point(3, 1)\n'\
    'C = point(3.2, 4)\n'\
    'D = point(0.8, 3)\n'\
    '\n'\
    'draw\n'\
    '  (A.B.C.D)\n'\
    '  $\\rotatebox{11}{\sffamily 4~cm}$ A 11 - 12.7 deg 4.1\n'\
    '  $\\rotatebox{86}{\sffamily 3~cm}$ B 86 - 8.9 deg 4.9\n'\
    '  $\\rotatebox{23}{\sffamily 2~cm}$ C 203 - 12.2 deg 4.2\n'\
    '  $\\rotatebox{83}{\sffamily 6.5~cm}$ D 263 - 12.9 deg 4.1\n'\
    '  $\\rotatebox{47.3}{\sffamily 64\\textdegree}$ A 47.3 deg 2.7\n'\
    '  $\\rotatebox{-41.3}{\sffamily 128\\textdegree}$ B 138.7 deg 2.7\n'\
    '  $\\rotatebox{54.3}{\sffamily 32\\textdegree}$ C 234.3 deg 2.7\n'\
    '  $\\rotatebox{322.7}{\sffamily 256\\textdegree}$ D 322.7 deg 2.7\n'\
    '  "A" A 227.3 deg, font("sffamily")\n'\
    '  "B" B 318.7 deg, font("sffamily")\n'\
    '  "C" C 54.3 deg, font("sffamily")\n'\
    '  "D" D 142.7 deg, font("sffamily")\n'\
    'end\n\n'\
    'label\n'\
    '  B, A, D simple\n'\
    '  C, B, A simple\n'\
    '  D, C, B simple\n'\
    '  A, D, C simple\n'\
    'end'
