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

from lib import error
from lib.common.cst import *

# -----------------------------------------------------------------------------
# ----------------------------------------- CLASS: sheet.S_Structure ----------
# -----------------------------------------------------------------------------
##
# @class S_Structure
# @brief Abstract mother class of all sheets !
# The constructor only has to be reimplemented, it is useless to reimplement
# other methods
class S_Structure(object):




    # -------------------------------------------------- CONSTRUCTOR ----------
    ##
    #   @brief /!\ Must be redefined. Constructor.
    #   @warning Exception NotInstanciableObject.
    #   @param embedded_machine The machine to be used
    #   @param **options Any options
    def __init__(self, embedded_machine, font_size_offset,
                 sheet_layout_unit, sheet_layout, layout_type,
                 **options):
        try:
            self.derived
        except AttributeError:
            raise error.NotInstanciableObject(self)

        self.machine = embedded_machine.clone(embedded_machine.language_code)
        self.machine.set_redirect_output_to_str(True)
        self.exercises_list = list()
        self.machine.set_font_size_offset(font_size_offset)

        self.sheet_layout_unit = sheet_layout_unit
        self.layout_type = layout_type
        self.write_texts_twice = False

        if 'write_texts_twice' in options \
            and options['write_texts_twice'] in YES:
        #___
            self.write_texts_twice = True

        # Some tests on sheet_layout before using it ;
        # but it's a bit complicated to write a complete set of tests on it ;
        # e.g. if the user doesn't use the same number of exercises in the
        # 'exc' key as in 'ans' key (which would be stupid) this
        # won't be checked here and so it won't work.
        if type(sheet_layout) != dict:
            raise error.UncompatibleType(str(type(sheet_layout)),
                                         'dict')

        if len(sheet_layout) != 2:
            raise error.WrongArgument('SHEET_LAYOUT should have two keys',
                                      'it has ' + str(len(sheet_layout)) \
                                      + ' keys')

        for k in ['exc', 'ans']:
            if not k in sheet_layout:
                raise error.WrongArgument('SHEET_LAYOUT should have a key ' \
                                          + k,
                                          'it has no such key')

            if type(sheet_layout[k]) != list:
                raise error.WrongArgument('SHEET_LAYOUT[' + k + '] should be' \
                                          + ' a list',
                                          str(type(sheet_layout[k])))

            if len(sheet_layout[k]) % 2:
                raise error.WrongArgument('SHEET_LAYOUT[' + k + '] should have'\
                                          + ' an even number of elements',
                                          str(len(sheet_layout[k])) \
                                          + ' elements')

            for i in xrange(len(sheet_layout[k]) / 2):
                if not (sheet_layout[k][2*i] is None \
                    or type(sheet_layout[k][2*i])== list \
                    or sheet_layout[k][2*i] == 'jump'):
                #___
                    raise error.WrongArgument('SHEET_LAYOUT[' + k + '][' \
                                              + str(2*i) + '] should be either'\
                                              + ' a list or None or "jump"',
                                              str(type(sheet_layout[k][2*i]))
                                              )
                elif sheet_layout[k][2*i] is None:
                    if not (type(sheet_layout[k][2*i+1]) == int \
                        or sheet_layout[k][2*i+1] == 'all' \
                        or sheet_layout[k][2*i+1] == 'all_left' \
                        or sheet_layout[k][2*i+1] == 'jump'):
                    #___
                        raise error.WrongArgument('SHEET_LAYOUT[' + k + '][' \
                                              + str(2*i+1) + '] should be an '\
                                              + 'int since it follows the None'\
                                              + 'keyword',
                                              type(sheet_layout[k][2*i+1]))

                elif sheet_layout[k][2*i] == 'jump':
                    if not sheet_layout[k][2*i+1] == 'next_page':
                        raise error.WrongArgument('SHEET_LAYOUT[' + k + '][' \
                                              + str(2*i+1) + '] should be : '\
                                              + 'next_page since it follows ' \
                                              + 'the jump' \
                                              + ' keyword',
                                              type(sheet_layout[k][2*i+1]))

                elif type(sheet_layout[k][2*i]) == list:
                    if not type(sheet_layout[k][2*i+1]) == tuple:
                        raise error.WrongArgument('SHEET_LAYOUT[' + k + '][' \
                                              + str(2*i+1) + '] should be a '\
                                              + 'tuple',
                                              type(sheet_layout[k][2*i+1]))

                    if not len(sheet_layout[k][2*i+1]) \
                       == (len(sheet_layout[k][2*i])-1)*sheet_layout[k][2*i][0]:
                    #___
                        raise error.WrongArgument('SHEET_LAYOUT[' + k + '][' \
                                              + str(2*i+1) + '] should have ' \
                                              + ' as many elements as the ' \
                                              + 'number of cols described in '\
                                              + 'SHEET_LAYOUT[' + k + '][' \
                                              + str(2*i) + ']',
                                              str(len(sheet_layout[k][2*i+1])) \
                                              + ' instead of ' \
                                              + str(len(sheet_layout[k][2*i]) \
                                                    - 1)
                                              )
                else:
                    raise error.WrongArgument('SHEET_LAYOUT[' + k + '][' \
                                              + str(2*i) + '] is not of any ' \
                                              + ' of the expected types or ' \
                                              + 'values.',
                                              str(len(sheet_layout[k][2*i]))
                                              )

        self.sheet_layout = sheet_layout





    # ----------------------------- OUTPUT WRITING : the whole sheet ----------
    ##
    #   @brief Writes the whole sheet's content to the output.
    def __str__(self):
        result = ""
        if self.layout_type == 'std' or self.layout_type == 'equations':
            result += self.machine.write_document_header()
            result += self.machine.write_document_begins()
            result += self.sheet_header_to_str()
            result += self.sheet_title_to_str()
            result += self.sheet_text_to_str()
            result += self.texts_to_str('exc', 0)
            result += self.machine.write_jump_to_next_page()
            result += self.answers_title_to_str()
            result += self.texts_to_str('ans', 0)
            result += self.machine.write_document_ends()

        elif self.layout_type == 'short_test':
            result += self.machine.write_document_header()
            result += self.machine.write_document_begins()

            n = 1
            if self.write_texts_twice:
                n = 2

            for i in xrange(n):
                result += self.sheet_header_to_str()
                result += self.sheet_title_to_str()
                result += self.sheet_text_to_str()
                result += self.texts_to_str('exc', 0)
                result += self.machine.write_new_line_twice()

                result += self.sheet_header_to_str()
                result += self.sheet_title_to_str()
                result += self.sheet_text_to_str()
                result += self.texts_to_str('exc', len(self.exercises_list)/2)
                result += self.machine.write_new_line_twice()

                if n == 2 and i == 0:
                    result += self.machine.insert_dashed_hline()
                    result += self.machine.write_new_line()
                    result += self.machine.insert_vspace()
                    result += self.machine.write_new_line_twice()


            result += self.machine.write_jump_to_next_page()

            result += self.answers_title_to_str()
            result += self.texts_to_str('ans', 0)
            result += self.machine.write_jump_to_next_page()
            result += self.answers_title_to_str()
            result += self.texts_to_str('ans', len(self.exercises_list)/2)
            result += self.machine.write_document_ends()

        elif self.layout_type == 'mini_test':
            result += self.machine.write_document_header()
            result += self.machine.write_document_begins()

            for i in xrange(3):
                result += self.sheet_header_to_str()
                result += self.sheet_title_to_str()
                result += self.sheet_text_to_str()
                result += self.texts_to_str('exc', 0)
                result += self.machine.write_new_line_twice()
                result += self.sheet_header_to_str()
                result += self.sheet_title_to_str()
                result += self.sheet_text_to_str()
                result += self.texts_to_str('exc', len(self.exercises_list)/2)
                result += self.machine.write_new_line_twice()


            #result += self.sheet_header_to_str()
            #result += self.sheet_title_to_str()
            #result += self.sheet_text_to_str()
            #result += self.texts_to_str('exc', len(self.exercises_list)/2)
            #result += self.machine.write_new_line_twice()
            #result += self.sheet_header_to_str()
            #result += self.sheet_title_to_str()
            #result += self.sheet_text_to_str()
            #result += self.texts_to_str('exc', 3*len(self.exercises_list)/4)

            result += self.machine.write_jump_to_next_page()

            result += self.answers_title_to_str()
            result += self.texts_to_str('ans', 0)
            result += self.machine.write_jump_to_next_page()
            result += self.answers_title_to_str()
            result += self.texts_to_str('ans', len(self.exercises_list)/2)


            #result += self.machine.write_jump_to_next_page()
            #result += self.answers_title_to_str()
            #result += self.texts_to_str('ans', len(self.exercises_list)/2)
            #result += self.machine.write_jump_to_next_page()
            #result += self.answers_title_to_str()
            #result += self.texts_to_str('ans', 3*len(self.exercises_list)/4)

            result += self.machine.write_document_ends()

        elif self.layout_type == 'mini_training':
            result += self.machine.write_document_header()
            result += self.machine.write_document_begins()

            for i in xrange(6):
                result += self.texts_to_str('exc', 0)
                result += self.machine.write_new_line_twice()

            result += self.machine.write_jump_to_next_page()

            result += self.answers_title_to_str()
            result += self.texts_to_str('ans', 0)

            result += self.machine.write_document_ends()

        elif self.layout_type == 'mental':
            result += self.machine.write_document_header()
            result += self.machine.write_document_begins()
            result += self.sheet_header_to_str()
            result += self.sheet_title_to_str()
            result += self.sheet_text_to_str()
            result += self.texts_to_str('exc', 0)
            result += self.machine.write_document_ends()

        else:
            raise error.OutOfRangeArgument(self.layout_type,
                                "std|short_test|mini_test|equations|mental")

        return result





    # ------------------------------ EXERCISES'|ANSWERS' TEXTS --> STR ---------
    ##
    #   @brief Return as str exercises' or answers'texts
    def texts_to_str(self, ex_or_answers, n_of_first_ex):
        M = self.machine

        result = ""

        result += M.reset_exercises_counter()
        result += M.write_set_font_size_to('large')
        layout = self.sheet_layout[ex_or_answers]

        ex_n = n_of_first_ex

        for k in xrange(len(layout) /2):
            if layout[2*k] is None:
                how_many = layout[2*k+1]

                if layout[2*k+1] == 'all_left' or layout[2*k+1] == 'all':
                    how_many = len(self.exercises_list) - ex_n
                    if (self.layout_type == 'short_test' \
                        or self.layout_type == 'mini_test') \
                        and ex_n < len(self.exercises_list) / 2:
                    #___
                        how_many = len(self.exercises_list) / 2 - ex_n
                    #elif self.layout_type == 'mini_test':
                    #    if ex_n < len(self.exercises_list) / 4:
                    #        how_many = len(self.exercises_list) / 4 - ex_n
                    #    elif ex_n < len(self.exercises_list) / 2:
                    #        how_many = len(self.exercises_list) / 2 - ex_n
                    #    elif ex_n < 3*len(self.exercises_list) / 4:
                    #        how_many = 3*len(self.exercises_list) / 4 - ex_n

                for i in xrange(how_many):
                    if not self.layout_type == 'mental':
                        result += M.write_exercise_number()
                    result += self.exercises_list[ex_n].to_str(ex_or_answers)
                    result += M.write_new_line(check=result[len(result)-2:])
                    #if not (ex_or_answers == 'ans' \
                    #    and self.layout_type == 'equations'):
                    #___
                    #    result += M.write_new_line()
                    ex_n += 1

            elif layout[2*k] == 'jump' and layout[2*k+1] == 'next_page':
                result += M.write_jump_to_next_page()

            else:
                nb_of_lines = layout[2*k][0]
                nb_of_cols = len(layout[2*k]) - 1
                col_widths = layout[2*k][1:len(layout[2*k])]
                content = []
                for i in xrange(nb_of_lines):
                    for j in xrange(nb_of_cols):
                        nb_of_ex_in_this_cell = layout[2*k + 1][i*nb_of_cols+j]
                        cell_content = ""
                        for n in xrange(nb_of_ex_in_this_cell):
                            if not self.layout_type == 'mental':
                                cell_content += M.write_exercise_number()
                            cell_content += \
                                self.exercises_list[ex_n].to_str(ex_or_answers)
                            ex_n += 1
                        content += [cell_content]

                result += M.write_layout((nb_of_lines, nb_of_cols),
                                          col_widths,
                                          content)

        return result



    # ------------------------------- OUTPUT WRITING : sheet's header ---------
    ##
    #   @brief Writes to the output the header of the sheet to be generated
    #   This header is written in a large size. A new line follow it.
    #   It's useful to write headers for test sheets, for example.
    def sheet_header_to_str(self):
        result = ""
        if self.header != "":
            result += self.machine.write_set_font_size_to('large')
            result += self.header
            result += self.machine.write_new_line()

        return result




    # -------------------------------- OUTPUT WRITING : sheet's title ---------
    ##
    #   @brief Writes to the output the title of the sheet to be generated
    def sheet_title_to_str(self):
        result = ""
        result += self.machine.write_set_font_size_to('LARGE')
        result += self.machine.write(self.title, emphasize='bold')
        if self.subtitle != "":
            result += self.machine.write_new_line()
            result += self.machine.write(self.subtitle, emphasize='bold')
        result += self.machine.write_new_line_twice()

        return result





    # ----------------------------------- OUTPUT WRITING : sheet text ---------
    ##
    #   @brief Writes to the output the sheet's text
    def sheet_text_to_str(self):
        result = ""
        if self.text != "":
            result += self.machine.write(self.text)
            result += self.machine.write_new_line_twice()

        return result






    # ------------------------------- OUTPUT WRITING : answers' title ---------
    ##
    #   @brief Writes to the output title of the answers' sheet to be generated
    def answers_title_to_str(self):
        result = ""

        result += self.machine.write_set_font_size_to('LARGE')
        result += self.machine.write(self.answers_title, emphasize='bold')
        result += self.machine.write_new_line_twice()

        return result





    # ---------------------------------------- OUTPUT WRITING : texts ---------
    ##
    #   @brief Writes to the output all exercises' texts
    #def write_texts(self):
    #    self.machine.reset_exercises_counter()
    #    self.machine.write_set_font_size_to('large')
    #    for e in self.exercises_list:
    #        self.machine.write_exercise_number()
    #        e.write_text()
    #        self.machine.write_new_line()





    # -------------------------------------- OUTPUT WRITING : answers ---------
    ##
    #   @brief Writes to the output all exercises' answers
    #def write_answers(self):
    #    self.machine.reset_exercises_counter()
    #    self.machine.write_set_font_size_to('large')
    #    for e in self.exercises_list:
    #        self.machine.write_exercise_number()
    #        e.write_answer()
    #        self.machine.write_new_line()





