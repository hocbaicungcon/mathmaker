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

from lib import shared
from lib import *
from settings import default
from . import question
# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class X_Structure
# @brief Mother class of all exercises objects. Not instanciable.
# This class suggests two default methods which are also in the exercise.Model
# class: write_text and write_answer. In a new exercise, they can either be
# kept untouched (then it would be wise to delete them from the new exercise)
# or rewritten.
class X_Structure(object):





    # --------------------------------------------------------------------------
    ##
    #   @brief /!\ Must be redefined. Constructor.
    #   @warning Exception NotInstanciableObject.
    #   @param **options Any options
    def __init__(self, x_kind, AVAILABLE_X_KIND_VALUES, X_LAYOUTS,
                 X_LAYOUT_UNIT, number_of_questions=6, **options):
        try:
            self.derived
        except AttributeError:
            raise error.NotInstanciableObject(self)

        self.questions_list = list()

        # OPTIONS -------------------------------------------------------------
        # It is necessary to define an options field to pass the
        # possibly modified value to the child class
        self.options = options

        try:
            AVAILABLE_X_KIND_VALUES[x_kind]
        except KeyError:
            raise error.OutOfRangeArgument(x_kind, str(AVAILABLE_X_KIND_VALUES))

        x_subkind = 'default'
        if 'x_subkind' in options:
            x_subkind = options['x_subkind']
            # let's remove this option from the options
            # since we re-use it recursively
            temp_options = dict()
            for key in options:
                if key != 'x_subkind':
                    temp_options[key] = options[key]
            self.options = temp_options

        if not x_subkind in AVAILABLE_X_KIND_VALUES[x_kind]:
            raise error.OutOfRangeArgument(x_subkind,
                                           str(AVAILABLE_X_KIND_VALUES[x_kind]))

        self.x_kind = x_kind
        self.x_subkind = x_subkind

        # Start number
        self.start_number = 0
        if 'start_number' in options:
            if not is_.an_integer(options['start_number']):
                raise error.UncompatibleType(options['start_number'],
                                             "integer")
            if not (options['start_number'] >= 1):
                raise error.OutOfRangeArgument(options['start_number'],
                                               "should be >= 1")

            self.start_number = options['start_number']

        # Number of questions
        if (not isinstance(number_of_questions, int)
            and number_of_questions >= 1):
        #___
            raise ValueError("The number_of_questions keyword argument should "
                             "be an int and greater than 6.")
        self.q_nb = number_of_questions


        self.x_layout_unit = X_LAYOUT_UNIT

        if (self.x_kind, self.x_subkind) in X_LAYOUTS:
            self.x_layout = X_LAYOUTS[(self.x_kind, self.x_subkind)]

        else:
            self.x_layout = X_LAYOUTS['default']


        # The slideshow option (for MentalCalculation sheets)
        self.slideshow = False

        if 'slideshow' in options and options['slideshow'] in YES:
            self.slideshow = True

        # END OF OPTIONS ------------------------------------------------------







    # --------------------------------------------------------------------------
    ##
    #   @brief Writes the text of the exercise|answer to the output.
    def to_str(self, ex_or_answers):
        M = shared.machine
        layout = self.x_layout[ex_or_answers]

        result = ""
        if self.text[ex_or_answers] != "":
            result += self.text[ex_or_answers]
            result += M.write_new_line()

        q_n = 0

        for k in range(int(len(layout) // 2)):
            if layout[2*k] is None:
                how_many = layout[2*k+1]
                if layout[2*k+1] == 'all_left' or layout[2*k+1] == 'all':
                    how_many = len(self.questions_list) - q_n
                for i in range(how_many):
                    result += self.questions_list[q_n].to_str(ex_or_answers)
                    if ex_or_answers == 'ans':
                        result += M.write_new_line(check=result[len(result)-2:])
                    q_n += 1
            else:
                nb_of_cols = len(layout[2*k]) - 1
                col_widths = layout[2*k][1:len(layout[2*k])]
                nb_of_lines = layout[2*k][0]
                if nb_of_lines == '?':
                    nb_of_lines = len(self.questions_list) // nb_of_cols + \
                        (0 if not len(self.questions_list) % nb_of_cols else 1)
                content = []
                for i in range(int(nb_of_lines)):
                    for j in range(nb_of_cols):
                        if layout[2*k+1] == 'all':
                            nb_of_q_in_this_cell = 1
                        else:
                            nb_of_q_in_this_cell = layout[2*k+1][i*nb_of_cols+j]
                        cell_content = ""
                        for n in range(nb_of_q_in_this_cell):
                            empty_cell = False
                            if q_n >= len(self.questions_list):
                                cell_content += " "
                                empty_cell = True
                            else:
                                cell_content += self.questions_list[q_n].\
                                                           to_str(ex_or_answers)
                            if ex_or_answers == 'ans' and not empty_cell:
                                cell_content += M.write_new_line(\
                                       check=cell_content[len(cell_content)-2:])
                            q_n += 1
                        content += [cell_content]

                result += M.write_layout((nb_of_lines, nb_of_cols),
                                          col_widths,
                                          content)

        return result