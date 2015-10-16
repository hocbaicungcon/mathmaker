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

import shlex
import xml.etree.ElementTree as XML_PARSER
from decimal import Decimal
import copy
import random
from collections import deque

import sys

from lib import *
from lib.common import default
import sheet
from .X_Structure import X_Structure
from . import question

# Here the list of available values for the parameter x_kind='' and the
# matching x_subkind values
AVAILABLE_X_KIND_VALUES = \
    {'tabular' : 'default',
     'slideshow' : 'default'
    }

MAX_NB_OF_QUESTIONS = 40

X_LAYOUT_UNIT = "cm"
# ----------------------  lines_nb    col_widths   questions
X_LAYOUTS = {'default' :
              { 'exc' : [ None,                    'all'
                        ],
                'ans' : [ None,                    'all'
                        ]
              }
            }


# --------------------------------------------------------------------------
##
#   @brief Gets the questions' kinds from the given file.
def get_q_kinds_from_file(file_name):

    try:
        xml_config = XML_PARSER.parse(file_name).getroot()
    except FileNotFoundError:
        raise error.UnreachableData("the file named : " + str(file_name))

    questions = []

    # For instance we will get a list of this kind of elements:
    # [ {'kind': 'multi', 'subkind': 'direct', 'nb': 'int'}, 'table_2_9', 4]

    x_kind = 'tabular' # default

    for child in xml_config:
        if child.tag == 'exercise':
            if 'kind' in child.attrib:
                x_kind = child.attrib['kind']
            for question in child:
                for elt in question:
                    questions += [[question.attrib,
                                   elt.tag, int(elt.text)]]

    return (x_kind, questions)

# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class X_MentalCalculation
# @brief Creates a tabular with n questions and answers
class X_MentalCalculation(X_Structure):





    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor.
    #   @param embedded_machine The machine that will be used to write output.
    #   @param **options Options detailed below :
    #          - start_number=<integer>
    #                         (should be >= 1)
    #          - number_of_questions=<integer>
    #            /!\ only useful if you use x_kind and not preformatted
    #                         (should be >= 1)
    #          - x_kind=<string>
    #                         ...
    #                         ...
    #          - preformatted=<string>
    #            /!\ preformatted is useless with short_test
    #            /!\ number_of_questions is useless with preformatted
    #            /!\ if you use it with the x_kind option, ensure there's a
    #                preformatted possibility with this option
    #                         'yes'
    #                         'OK'
    #                         any other value will be understood as 'no'
    #          - short_test=<string>
    #            /!\ the x_kind option above can't be used along this option
    #            use subtype if you need to make different short_test exercises
    #                         'yes'
    #                         'OK'
    #                         any other value will be understood as 'no'
    #          - subtype=<string>
    #                         ...
    #                         ...
    #   @todo Complete the description of the possible options !
    #   @return One instance of exercise.X_MentalCalculation
    def __init__(self, embedded_machine, x_kind='default_nothing', **options):
        self.derived = True
        mc_mm_file = options['filename'] if 'filename' in options \
                                         else sheet.catalog.XML_SHEETS[\
                                                  'mental_calculation_default']

        (x_kind, q_list) = get_q_kinds_from_file(mc_mm_file)

        X_Structure.__init__(self, embedded_machine,
                             x_kind, AVAILABLE_X_KIND_VALUES, X_LAYOUTS,
                             X_LAYOUT_UNIT, **options)
        # The purpose of this next line is to get the possibly modified
        # value of **options
        options = self.options

        # BEGINING OF THE ZONE TO REWRITE (see explanations below) ------------

        # should be default_question = question.Something
        default_question = question.Q_MentalCalculation

        # TEXTS OF THE EXERCISE
        self.text = {'exc' : "",
                     'ans' : ""
                    }

        # From q_list, we build a dictionary:
        q_dict = {}

        nb_box = {}
        nb_used = {}
        last_nb = {}

        self.q_nb = 0

        # In q_list, each element is like this:
        # [{'kind':'multi', 'subkind':'direct', 'nb':'int'}, 'table_2_9', 4]
        # [q[0],                                             q[1],        q[2]]
        for q in q_list:
            if not q[1] in nb_box:
                nb_box[q[1]] = question.generate_numbers(q[1])
                nb_used[q[1]] = []
                last_nb[q[1]] = []

            self.q_nb += q[2]

            for n in range(q[2]):
                q_id = q[0]['kind']
                q_id += "_"
                q_id += q[0]['subkind']
                q_options = copy.deepcopy(q[0])
                del q_options['kind']
                del q_options['subkind']
                if not q_id in q_dict:
                    q_dict[q_id] = []
                q_dict[q_id] += [(q[1], q_options)]

        # Now, q_dict is organized like this:
        # { 'multi_direct' :   [('table_2_9', {'nb':'int'}),
        #                       ('table_2_9', {'nb':'int'})],
        #   'multi_reversed' : [('table_2_9', {'nb':'int'})],
        #   'divi_direct' :    [('table_2_9', {'nb':'int'})],
        #   'multi_hole' :     [('table_2_9', {'nb':'int'})],
        #   'q_id' :           [('table_15', {'nb':'int'})],
        #   'q_id :            [('table_25', {'nb':'int'})],
        #   'etc.'
        # }

        # We shuffle the lists a little bit:
        for key in q_dict:
            random.shuffle(q_dict[key])

        # Now we mix the questions types (by id):
        mixed_q_list = []
        q_id_box = copy.deepcopy(list(q_dict.keys()))
        q_ids_aside = deque()

        for n in range(self.q_nb):
            q_nb_in_q_id_box = sum([len(q_dict[q_id]) for q_id in q_dict])

            w_table = [Decimal(Decimal(len(q_dict[q_id])) \
                               / Decimal(q_nb_in_q_id_box)) \
                       for q_id in q_id_box]

            q_id = randomly.pop(q_id_box,
                                weighted_table=w_table)

            info = q_dict[q_id].pop(0)

            mixed_q_list += [(q_id, info[0], info[1])]

            if len(q_dict[q_id]):
                q_ids_aside.appendleft(q_id)
                if len(q_ids_aside) >= 4 or len(q_id_box) <= 1:
                    q_id_box += [q_ids_aside.pop()]
            else:
                del q_dict[q_id]

            if len(q_id_box) <= 1 and len(q_ids_aside) > 0:
                q_id_box += [q_ids_aside.pop()]

        # Now, mixed_q_list is organized like this:
        # [ ('multi_direct',   'table_2_9', {'nb':'int'}),
        #   ('multi_reversed', 'table_2_9', {'nb':'int'}),
        #   ('q_id',           'table_15',  {'nb':'int'}),
        #   ('multi_hole',     'table_2_9', {'nb':'int'}),
        #   ('multi_direct',   'table_2_9', {'nb':'int'}),
        #   ('q_id,            'table_25',  {'nb':'int'}),
        #   ('divi_direct',    'table_2_9', {'nb':'int'}),
        #   etc.
        # ]

        # Now, we generate the numbers & questions, by type of question first
        self.questions_list = []

        for q in mixed_q_list:
            (kept_aside, nb_box[q[1]]) = utils.put_aside(last_nb[q[1]],
                                                         nb_box[q[1]])

            if len(nb_box[q[1]]) == 0:
                nb_box[q[1]] = question.generate_numbers([q[1]])
                kept_aside = []

            nb_to_use = randomly.pop(nb_box[q[1]])

            nb_box[q[1]] += kept_aside

            self.questions_list += [default_question(embedded_machine,
                                                     q[0],
                                                     q[2],
                                                     numbers_to_use=nb_to_use
                                                     )]

            last_nb[q[1]] = []
            if q[1] == 'table_2_9':
                last_nb[q[1]] += [nb_to_use[0], nb_to_use[1]]
            elif q[1] == 'int_irreducible_frac':
                last_nb[q[1]] += [nb_to_use[0]]
            else:
                last_nb[q[1]] += [nb_to_use[1]]


        # END OF THE ZONE TO REWRITE ------------------------------------------





    # --------------------------------------------------------------------------
    ##
    #   @brief Writes the text of the exercise|answer to the output.
    def to_str(self, ex_or_answers):
        M = self.machine
        result = ""

        if self.slideshow:
            result += M.write_frame("", frame='start_frame')
            for i in range(self.q_nb):
                result += M.write_frame(self.questions_list[i].to_str('exc'),
                                    timing=self.questions_list[i].transduration)

            result += M.write_frame("", frame='middle_frame')

            for i in range(self.q_nb):
                result += M.write_frame(_("Question:") \
                                        + self.questions_list[i].to_str('exc')\
                                        + _("Answer:") \
                                        + self.questions_list[i].to_str('ans'),
                                        timing=0)

        # default tabular option:
        else:
            q = [self.questions_list[i].to_str('exc') for i in range(self.q_nb)]
            a = [self.questions_list[i].to_str('ans') for i in range(self.q_nb)]\
                if ex_or_answers == 'ans' else [" " for i in range(self.q_nb)]

            content = [elt for pair in zip(q, a) for elt in pair]

            result += M.write_layout((self.q_nb, 2),
                                     [14, 4],
                                     content,
                                     borders='all',
                                     center='yes',
                                     center_vertically='yes')

        return result





    # INSTRUCTIONS TO CREATE A NEW EXERCISE -----------------------------------
    # - Indicate its name in the header comment
    #   the one of documentation (@class)
    # - Write the @brief description
    # - Replace the Model class name by the chosen one
    # - In the constructor comment, replace Model with the chosen name
    #   at the @return line
    # - Write the class name of the default_question. You must mention it
    #   because it will be used in the OTHER EXERCISES section.
    # - The different sections to rewrite are :
    #   * TEXTS OF THE EXERCISE:
    #       default text for all exercises of this class
    #   * alternate texts section:
    #       if you want to specify a different text for any particular kind
    #       of exercise
    #   * PREFORMATTED EXERCISES
    #       that's where preformatted exercises are described (the ones that
    #       won't repeat n times the same kind of randomly question)
    #   * OTHER EXERCISES section is meant to all exercises that repeat
    #       the same (maybe randomly chosen among many) kind of question.
    #       shouldn't be rewritten
    # - Finally, if the write_* methods from the exercise.Structure don't
    #   match your needs, copy & modify or rewrite them
