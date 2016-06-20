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

from mathmaker.lib import *
from .X_Structure import X_Structure
from . import question

# Here the list of available values for the parameter x_kind='' and the
# matching x_subkind values
# Note: the bypass value allows to give the value of *x_subkind* directly to
# the matching question Constructor, bypassing the action of the present class
AVAILABLE_X_KIND_VALUES = \
    {#'short_test': ['x_subkind1', 'x_subkind2'],
     'preformatted': ['fraction_simplification', 'fractions_product',
                       'fractions_quotient', 'fractions_sum']
     #'bypass': ['']
    }

X_LAYOUT_UNIT = "cm"
# ----------------------  lines_nb  col_widths             questions
X_LAYOUTS = {'default':
              { 'exc': [ ['?',     9, 9],                 'all'
                        ],
                'ans': [ ['?',     6, 6, 6],              'all'
                        ]
              }

            }

# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class X_Calculation
# @brief Calculation questions (calculate: 2-(3+5)×4, simplify a fraction...)
class X_Calculation(X_Structure):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor.
    #   @param **options Any options
    #   @return One instance of exercise.Calculation
    def __init__(self, x_kind='default_nothing', **options):
        self.derived = True
        X_Structure.__init__(self,
                             x_kind, AVAILABLE_X_KIND_VALUES, X_LAYOUTS,
                             X_LAYOUT_UNIT, **options)
        # The purpose of this next line is to get the possibly modified
        # value of **options
        options = self.options

        default_question = question.Q_Calculation

        # TEXTS OF THE EXERCISE
        self.text = {'exc': "",
                     'ans': ""
                    }

        # alternate texts section
        if self.x_kind == 'preformatted':
            if self.x_subkind == 'fraction_simplification':
                self.text = {'exc': _("Simplify the following fractions:"),
                             'ans': ""
                            }
            elif self.x_subkind == 'fractions_product' \
                 or self.x_subkind == 'fractions_quotient' \
                 or self.x_subkind == 'fractions_sum':
                # __
                self.text = {'exc': _( \
                    "Calculate and give the result as a simplified fraction:"),
                             'ans': ""
                            }

        # PREFORMATTED EXERCISES
        if self.x_kind == 'preformatted':
            if self.x_subkind == 'fraction_simplification':
                #self.text = _("Simplify the following fractions:")

                for i in range(int(self.q_nb // 2)):
                    q=question.Q_Calculation(
                                           self.x_subkind,
                                           expression_number=i,
                                           **options)

                    self.questions_list.append(q)

                for i in range(self.q_nb - int(self.q_nb // 2)):
                    q=question.Q_Calculation(
                                          self.x_subkind,
                                          expression_number=i+int(self.q_nb//2),
                                          with_ten_powers=0.3,
                                          **options)

                    self.questions_list.append(q)

            elif self.x_subkind == 'fractions_product' \
                 or self.x_subkind == 'fractions_quotient' \
                 or self.x_subkind == 'fractions_sum':
                # __
                #self.text = _( \
                #    "Calculate and give the result as a simplified fraction:")

                for i in range(self.q_nb):
                    q=question.Q_Calculation(
                                           self.x_subkind,
                                           expression_number=i,
                                           **options)

                    self.questions_list.append(q)

