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

import random

from core.base_calculus import *
from core.root_calculus import Value
from . import mc_module
from lib.tools.wordings_handling import setup_wording_format_of

class sub_object(mc_module.structure):

    def __init__(self, M, numbers_to_use, **options):
        super().setup(M, "minimal", **options)
        super().setup(M, "length_units", **options)

        if self.context == "from_area":
            super().setup(M, "division", nb=numbers_to_use, **options)
            self.nb1, self.nb2 = self.dividend, self.divisor
            super().setup(M, "rectangle", **options)
            wordings = {'w': _("A rectangle has an area of {nb1} {area_unit} \
and a length of {nb2} {length_unit}. What is its width? |hint:length_unit|"),
                        'l': _("A rectangle has an area of {nb1} {area_unit} \
and a width of {nb2} {length_unit}. What is its length? |hint:length_unit|")
                       }
            self.wording = wordings[self.subcontext]
            setup_wording_format_of(self, M)

        elif self.context == "from_perimeter":
            super().setup(M, "numbers", nb=numbers_to_use, **options)
            super().setup(M, "nb_variants", nb=numbers_to_use, **options)
            super().setup(M, "rectangle", **options)
            self.subcontext = random.choice(['w', 'l'])
            self.nb1 = self.rectangle.perimeter
            self.nb2, self.nb3 = (self.rectangle.width, self.rectangle.length)\
                                 if self.subcontext == 'l'\
                                 else (self.rectangle.length, \
                                      self.rectangle.width)
            self.result = self.nb3
            wordings = { 'w': _("What is the width of a rectangle whose \
perimeter is {nb1} {length_unit} and length is {nb2} {length_unit}? \
|hint:length_unit|"),
                         'l': _("What is the length of a rectangle whose \
perimeter is {nb1} {length_unit} and width is {nb2} {length_unit}? \
|hint:length_unit|")
                       }
            self.wording = wordings[self.subcontext]
            setup_wording_format_of(self, M)

        else:
            raise error.ImpossibleAction("Create this question without any "\
                                         + "context.")

        if self.subcontext == "w":
            self.rectangle.setup_labels([False, False, True, "?"])
        elif self.subcontext == "l":
            self.rectangle.setup_labels([False, False, "?", True])

    def q(self, M, **options):
        if self.picture:
            return M.write_layout((1, 2),
                                  [3.5, 9.5],
                                  [M.insert_picture(self.rectangle,
                                                    scale=0.75,
                                     vertical_alignment_in_a_tabular=True),
                                   self.wording.format(**self.wording_format)])
        else:
            return self.wording.format(**self.wording_format)

    def a(self, M, **options):
        v = Value(self.result, unit=self.hint).into_str(display_SI_unit=True)
        return v
