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
from . import exercise

from .S_Structure import S_Structure

FONT_SIZE_OFFSET = -1
SHEET_LAYOUT_TYPE = 'std'
SHEET_LAYOUT_UNIT = "cm"
#EXAMPLE OF A SHEET NOT USING ANY LAYOUT
# -----------------------  lines_nb    col_widths   exercises
SHEET_LAYOUT = { 'exc' : [ None,                    'all'
                         ],
                 'ans' : [ None,                    'all'
                         ]
               }

# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class AlgebraMiniTest0
# @brief A simple algebra mini-test
class AlgebraMiniTest0(S_Structure):





    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor
    #   @param embedded_machine The machine to be used
    #   @param **options Any options
    #   @return One instance of sheet.Model
    def __init__(self, embedded_machine, **options):
        self.derived = True
        S_Structure.__init__(self, embedded_machine, FONT_SIZE_OFFSET,
                             SHEET_LAYOUT_UNIT, SHEET_LAYOUT,
                             SHEET_LAYOUT_TYPE)

        # BEGINING OF THE ZONE TO REWRITE (see explanations below) ------------
        self.header = ""
        #self.title = _("Training exercises sheet :")
        self.title = ""
        self.subtitle = ""
        self.text = ""
        self.answers_title = _("Examples of answers")

        # For instance :
        # ex1 = exercise.ProductReduction(self.machine, many=30)
        # self.exercises_list.append(ex1)

        for i in range(10):
            ex1 = exercise.X_AlgebraExpressionExpansion(self.machine,
                                                    x_kind='mini_test',
                                                    x_subkind='two_randomly')

            self.exercises_list.append(ex1)





        # END -----------------------------------------------------------------
        # Instructions for use (creating a new sheet) :
        # - Put its name in the header's comment
        #   & in the one of the documentation (@class)
        # - Write the @brief comment
        # - Replace Model by the chosen name
        # - Choose the values for the globals
        # - In the constructor's comment, replace Model by the chosen name at
        #   the @return line
        # - Skip to the zone to rewrite and for each exercise, follow the
        #   example (i.e. write on two lines :
        #   - ex_number_n = exercise.ThmPythagore(self.machine, options...)
        #   - self.exercises_list.append(ex_number_n)
        #   and so on with ex<n+1>, ex<n+2> as many as desired)
