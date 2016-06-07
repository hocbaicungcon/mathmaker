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

import sys
import pytest
import locale
import decimal

from lib.core.base_calculus import Item, SquareRoot
from tools import wrap_nb


def test_sq5_printed():
    """Is SquareRoot(Item(5)) correctly printed?"""
    assert SquareRoot(Item(5)).printed == wrap_nb('\\sqrt{\\mathstrut 5}')


def test_sq5_next_step():
    """Is SquareRoot(Item(5)) calculation's next step correct?"""
    assert SquareRoot(Item(5)).calculate_next_step(decimal_result=4)\
           .printed == wrap_nb('2.2361')

def test_sq16_next_step():
    """Is SquareRoot(Item(16)) calculation's next step correct?"""
    assert SquareRoot(Item(16)).calculate_next_step(decimal_result=4)\
           .printed == wrap_nb('4')
