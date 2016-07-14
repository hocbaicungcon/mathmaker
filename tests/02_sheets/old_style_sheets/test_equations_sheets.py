# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2016 Nicolas Hainaux <nh.techn@gmail.com>

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

from mathmaker.lib import shared
from mathmaker.lib.sheet import AVAILABLE


def test_basic():
    """Checks if 'equations-basic' is generated without any error."""
    shared.machine.write_out(str(AVAILABLE['equations-basic'][0]()))


def test_classic():
    """Checks if 'equations-classic' is generated without any error."""
    shared.machine.write_out(str(AVAILABLE['equations-classic'][0]()))


def test_harder():
    """Checks if 'equations-harder' is generated without any error."""
    shared.machine.write_out(str(AVAILABLE['equations-harder'][0]()))


def test_test():
    """Checks if 'equations-test' is generated without any error."""
    shared.machine.write_out(str(AVAILABLE['equations-test'][0]()))


def test_short_test():
    """Checks if 'equations-short-test' is generated without any error."""
    shared.machine.write_out(str(AVAILABLE['equations-short-test'][0]()))
