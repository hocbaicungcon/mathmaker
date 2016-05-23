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

# This module will add a question about the sum of two numbers

from core.base_calculus import Sum
from . import vocabulary_questions

class sub_object(vocabulary_questions.structure):

    def __init__(self, M, numbers_to_use, **options):
        super().__init__(
            M, numbers_to_use,
            result_fct=lambda x,y: Sum([max(x, y), -min(x, y)]),
            wording=_("How much is the difference between {nb1} and {nb2}?"),
            **options)

