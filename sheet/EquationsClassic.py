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

import machine
import exercise

from S_Structure import S_Structure

FONT_SIZE_OFFSET = -1
SHEET_LAYOUT_TYPE = 'equations'
SHEET_LAYOUT_UNIT = "cm"
# -----------------------  lines_nb    col_widths   exercises
SHEET_LAYOUT = { 'exc' : [ None,                    'all'
                         ],
                 'ans' : [ None,                    1,
                           'jump',                  'next_page',
                           None,                    1
                         ]
               }

# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class EquationsClassic
# @brief Collection of basic equations to solve (like x+7=-9, 5x=10, 3=2-x...).
class EquationsClassic(S_Structure):





    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor
    #   @param embedded_machine The machine to be used
    #   @param **options Any options
    #   @return One instance of sheet.EquationsClassic
    def __init__(self, embedded_machine, **options):
        self.derived = True
        S_Structure.__init__(self, embedded_machine, FONT_SIZE_OFFSET,
                             SHEET_LAYOUT_UNIT, SHEET_LAYOUT,
                             SHEET_LAYOUT_TYPE)

        # BEGINING OF THE ZONE TO REWRITE (see explanations below) ------------
        self.header = ""
        self.title = _("Training exercises sheet :")
        self.subtitle = ""
        self.text = _("Solve the following equations.")
        self.answers_title = _("Examples of answers")


        ex1 = exercise.X_Equation(self.machine,
                                  x_kind='preformatted',
                                  x_subkind='classics')

        ex2 = exercise.X_Equation(self.machine,
                                  x_kind='preformatted',
                                  x_subkind='classic_xtwice_and_any')


        self.exercises_list.append(ex1)
        self.exercises_list.append(ex2)







    # END ---------------------------------------------------------------------
