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

import random

from lib import *
from lib.common.cst import *
from .Q_Structure import Q_Structure
from . import mc_modules
from core.base_calculus import *

SUBKINDS_TO_UNPACK = {'simple_parts_of_a_number': {'half', 'third', 'quarter'},
                      'simple_multiples_of_a_number': {'double', 'triple',
                                                        'quadruple'},
                      'simple_parts_or_multiples_of_a_number': {'half',
                                                                 'third',
                                                                 'quarter',
                                                                 'double',
                                                                 'triple',
                                                                 'quadruple'},
                      'operation': {'multi', 'divi', 'addi', 'subtr'}
                     }

UNPACKABLE_SUBKINDS = {'half', 'third', 'quarter',
                       'double', 'triple', 'quadruple',
                       'multi', 'divi', 'addi', 'subtr'
                      }

SOURCES_TO_UNPACK = {'auto_table': {'half': {'table_2'},
                                     'third': {'table_3'},
                                     'quarter': {'table_4'},
                                     'double': {'table_2'},
                                     'triple': {'table_3'},
                                     'quadruple': {'table_4'},
                                     'multi': {'intpairs_2to9'},
                                     'divi': {'intpairs_2to9'},
                                     'addi': {'intpairs_2to9'},
                                     'subtr': {'intpairs_2to9'}},
                     'auto_11_50': {'half': {'multiplesof2_11to50'},
                                     'third': {'multiplesof3_11to50'},
                                     'quarter': {'multiplesof4_11to50'},
                                     'double': {'multiplesof2_11to50'},
                                     'triple': {'multiplesof3_11to50'},
                                     'quadruple': {'multiplesof4_11to50'}},
                     'auto_vocabulary':  \
                               {'half': {'table_2', 'multiplesof2_11to50'},
                                'third': {'table_3', 'multiplesof3_11to50'},
                                'quarter': {'table_4', 'multiplesof4_11to50'},
                                'double': {'table_2', 'multiplesof2_11to50'},
                                'triple': {'table_3', 'multiplesof3_11to50'},
                                'quadruple': {'table_4', 'multiplesof4_11to50'},
                                'multi': {'intpairs_2to9'},
                                'divi': {'intpairs_2to9'},
                                # The 'intpairs_2to200' below will get divided
                                # by 10 to produce two decimals between 0.2
                                # and 20.
                                'addi': {'intpairs_10to100',
                                         'intpairs_2to200'},
                                'subtr': {'intpairs_10to100',
                                          'intpairs_2to200'}},
                     'decimal_and_10_100_1000': \
                {'multi_direct': {'decimal_and_10_100_1000_for_multi'},
                 'divi_direct': {'decimal_and_10_100_1000_for_divi'},
                 'area_rectangle': {'decimal_and_10_100_1000_for_multi'},
                 'perimeter_rectangle': {'decimal_and_10_100_1000_for_multi'},
                 'multi_hole': {'decimal_and_10_100_1000_for_multi'},
                 'vocabulary_multi': {'decimal_and_10_100_1000_for_multi'},
                 'vocabulary_divi': {'decimal_and_10_100_1000_for_divi'}
                 },
                     'decimal_and_one_digit': \
                 {'multi_direct': {'decimal_and_one_digit_for_multi'},
                  'divi_direct': {'decimal_and_one_digit_for_divi'},
                  'area_rectangle': {'decimal_and_one_digit_for_multi'},
                  'multi_hole': {'decimal_and_one_digit_for_multi'},
                  'vocabulary_multi': {'decimal_and_one_digit_for_multi'},
                  'vocabulary_divi': {'decimal_and_one_digit_for_divi'}
                  }
                     }

SOURCES_TO_TRANSLATE = {'subtr_direct': \
                            {'integers_10_100': 'integers_10_100_diff7atleast'}
                        }

MODULES =  \
    { 'multi_direct': mc_modules.multi_direct,
      'multi_reversed': mc_modules.multi_reversed,
      'multi_hole': mc_modules.multi_hole,
      'addi_direct': mc_modules.addi_direct,
      'subtr_direct': mc_modules.subtr_direct,
      'divi_direct': mc_modules.divi_direct,
      'rank_direct': mc_modules.rank_direct,
      'rank_reversed': mc_modules.rank_reversed,
      'rank_numberof': mc_modules.rank_numberof,
      'vocabulary_half': mc_modules.vocabulary_simple_part_of_a_number,
      'vocabulary_third': mc_modules.vocabulary_simple_part_of_a_number,
      'vocabulary_quarter': mc_modules.vocabulary_simple_part_of_a_number,
      'vocabulary_double': mc_modules.vocabulary_simple_multiple_of_a_number,
      'vocabulary_triple': mc_modules.vocabulary_simple_multiple_of_a_number,
      'vocabulary_quadruple': mc_modules.vocabulary_simple_multiple_of_a_number,
      'vocabulary_multi': mc_modules.vocabulary_multi,
      'vocabulary_divi': mc_modules.vocabulary_divi,
      'vocabulary_addi': mc_modules.vocabulary_addi,
      'vocabulary_subtr': mc_modules.vocabulary_subtr,
      'area_rectangle': mc_modules.area_rectangle,
      'perimeter_rectangle': mc_modules.perimeter_rectangle,
      'rectangle_length_or_width': mc_modules.rectangle_length_or_width,
      'perimeter_square': mc_modules.perimeter_square,
      'area_square': mc_modules.area_square
    }


# --------------------------------------------------------------------------
##
#   @brief Returns a list of numbers of the given kind
def generate_decimal(width, ranks_scale, start_rank):
    # Probability to fill a higher rank rather than a lower one
    phr = 0.5
    hr = lr = start_rank
    ranks = [start_rank]

    for i in range(width - 1):
        if lr == 0:
            phr = 1
        elif hr == len(ranks_scale) - 1:
            phr = 0

        if random.random() < phr:
            hr += 1
            ranks += [hr]
            phr *= 0.4
        else:
            lr -= 1
            ranks += [lr]
            phr *= 2.5

    figures = [str(i+1) for i in range(9)]

    deci = Decimal('0')

    for r in ranks:
        figure = randomly.pop(figures)
        deci +=  Decimal(figure) * ranks_scale[r]

    return deci


# --------------------------------------------------------------------------
##
#   @brief  Tells if the given question's type and source number do match
#   @todo   The 'integer_3_10_decimal_3_10' may be later turned into
#           'intpairs_3to10' with variant='decimal1', so this condition can
#           certainly be removed.
def match_qtype_sourcenb(q_type, source_nb):
    if q_type in ['multi_direct', 'area_rectangle', 'multi_hole',
                  'rectangle_length_or_width_from_area', 'divi_direct',
                  'vocabulary_multi', 'vocabulary_divi']:
    #___
        return any([source_nb.startswith('intpairs_'),
                    source_nb.startswith('multiplesof'),
                    source_nb.startswith('table_'),
                    source_nb == 'decimal_and_10_100_1000',
                    source_nb == 'decimal_and_one_digit',
                    source_nb == 'bypass'])
    elif q_type in ['addi_direct', 'subtr_direct', 'perimeter_rectangle',
                    'rectangle_length_or_width_from_perimeter',
                    'vocabulary_addi', 'vocabulary_subtr']:
    #___
        return any([source_nb.startswith('intpairs_'),
                    source_nb.startswith('multiplesof'),
                    source_nb.startswith('table_'),
                    source_nb == 'decimal_and_10_100_1000',
                    source_nb == 'integer_3_10_decimal_3_10',
                    source_nb == 'decimals_0_20_1',
                    source_nb == 'bypass'])
    elif q_type.startswith('rank_'):
        return any([source_nb == 'rank_words', source_nb == 'bypass'])
    elif q_type in ['perimeter_square', 'area_square']:
        return any([source_nb.startswith('intpairs_'),
                    source_nb.startswith('multiplesof'),
                    source_nb.startswith('table_'),
                    source_nb == 'bypass'])
    elif q_type in ['vocabulary_half', 'vocabulary_double']:
        return any([source_nb.startswith('multiplesof2'),
                    source_nb == 'table_2',
                    source_nb == 'bypass'])
    elif q_type in ['vocabulary_third', 'vocabulary_triple']:
        return any([source_nb.startswith('multiplesof3'),
                    source_nb == 'table_3',
                    source_nb == 'bypass'])
    elif q_type in ['vocabulary_quarter', 'vocabulary_quadruple']:
        return any([source_nb.startswith('multiplesof4'),
                    source_nb == 'table_4',
                    source_nb == 'bypass'])
    elif q_type == 'multi_reversed':
        return any([(source_nb.startswith('intpairs_')
                     and source_nb.endswith('to9')),
                    source_nb == 'table_2',
                    source_nb == 'table_3',
                    source_nb == 'table_4',
                    source_nb == 'bypass'])


# --------------------------------------------------------------------------
##
#   @brief Returns a dictionary to give some special informations needed for
#          certain questions.
def get_modifier(q_type):
    d = {}
    if q_type == 'multi_reversed':
        d.update({'multi_reversed': True,
                  'info_multirev': {(2, 6): [(2, 6), (3, 4)],
                                    (3, 4): [(2, 6), (3, 4)],
                                    (2, 8): [(2, 8), (4, 4)],
                                    (4, 4): [(2, 8), (4, 4)],
                                    (3, 6): [(3, 6), (2, 9)],
                                    (2, 9): [(3, 6), (2, 9)],
                                    (3, 8): [(3, 8), (4, 6)],
                                    (4, 6): [(3, 8), (4, 6)],
                                    (4, 9): [(4, 9), (6, 6)],
                                    (6, 6): [(4, 9), (6, 6)],
                                    }})
    elif 'rectangle' in q_type:
        d.update({'rectangle': True})
    elif 'square' in q_type:
        d.update({'square': True})
    return d

# --------------------------------------------------------------------------
##
#   @brief Returns a list of numbers of the given kind
def generate_numbers(subkind):
    if subkind == 'table_2_9' or subkind == 'table_2_9_for_sums_diffs':
        return {(2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9),
                (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9),
                (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9),
                (5, 5), (5, 6), (5, 7), (5, 8), (5, 9),
                (6, 6), (6, 7), (6, 8), (6, 9),
                (7, 7), (7, 8), (7, 9),
                (8, 8), (8, 9),
                (9, 9)}

    elif subkind == 'table_2_9_for_rectangles':
        return {(2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9),
                (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9),
                (4, 5), (4, 6), (4, 7), (4, 8), (4, 9),
                (5, 6), (5, 7), (5, 8), (5, 9),
                (6, 7), (6, 8), (6, 9),
                (7, 8), (7, 9),
                (8, 9)}

    elif subkind == 'table_2_9_for_multi_reversed':
        return {(2, 2), (2, 3), (2, 4), (2, 5), (2, 7),
                (3, 3), (3, 5), (3, 7), (3, 9),
                (4, 5), (4, 7), (4, 8),
                (5, 5), (5, 6), (5, 7), (5, 8), (5, 9),
                (6, 7), (6, 8), (6, 9),
                (7, 7), (7, 8), (7, 9),
                (8, 8), (8, 9),
                (9, 9),
                random.choice([(2, 6), (3, 4)]),
                random.choice([(2, 8), (4, 4)]),
                random.choice([(3, 6), (2, 9)]),
                random.choice([(3, 8), (4, 6)]),
                random.choice([(4, 9), (6, 6)])}

    elif subkind == 'squares_2_9':
        return {(2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)}

    elif subkind == 'table_4_9':
        return {(4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9),
                (5, 5), (5, 6), (5, 7), (5, 8), (5, 9),
                (6, 6), (6, 7), (6, 8), (6, 9),
                (7, 7), (7, 8), (7, 9),
                (8, 8), (8, 9),
                (9, 9)}

    elif subkind == 'table_4_9_for_rectangles':
        return {(4, 5), (4, 6), (4, 7), (4, 8), (4, 9),
                (5, 6), (5, 7), (5, 8), (5, 9),
                (6, 7), (6, 8), (6, 9),
                (7, 8), (7, 9),
                (8, 9)}

    elif subkind == 'table_4_9_for_multi_reversed':
        return {(4, 4), (4, 5), (4, 6), (4, 7), (4, 8),
                (5, 5), (5, 6), (5, 7), (5, 8), (5, 9),
                (6, 7), (6, 8), (6, 9),
                (7, 7), (7, 8), (7, 9),
                (8, 8), (8, 9),
                (9, 9),
                random.choice([(4, 9), (6, 6)])}

    elif subkind == 'squares_4_9':
        return {(4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)}

    elif subkind == 'table_2':
        return {(2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9)}

    elif subkind == 'table_3':
        return {(3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9)}

    elif subkind == 'table_4':
        return {(4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9)}

    elif subkind == 'table_2_11_50':
        return {(2, n+11) for n in range(40)}

    elif subkind == 'table_3_11_50':
        return {(3, n+11) for n in range(40)}

    elif subkind == 'table_4_11_50':
        return {(4, n+11) for n in range(40)}

    elif subkind == 'table_11':
        return {(11, 11), (11, 12), (11, 13), (11, 14), (11, 15), (11, 16),
                (11, 17), (11, 18),
                (11, 21), (11, 22), (11, 23), (11, 24), (11, 25), (11, 26),
                (11, 27),
                (11, 31), (11, 32), (11, 33), (11, 34), (11, 35), (11, 36),
                (11, 41), (11, 42), (11, 43), (11, 44), (11, 45),
                (11, 51), (11, 52), (11, 53), (11, 54),
                (11, 61), (11, 62), (11, 63),
                (11, 71), (11, 72),
                (11, 81)}

    elif subkind == 'table_11_for_rectangles':
        return {(11, 12), (11, 13), (11, 14), (11, 15), (11, 16),
                (11, 17), (11, 18),
                (11, 21), (11, 22), (11, 23), (11, 24), (11, 25), (11, 26),
                (11, 27),
                (11, 31), (11, 32), (11, 33), (11, 34), (11, 35), (11, 36),
                (11, 41), (11, 42), (11, 43), (11, 44), (11, 45),
                (11, 51), (11, 52), (11, 53), (11, 54),
                (11, 61), (11, 62), (11, 63),
                (11, 71), (11, 72),
                (11, 81)}

    elif subkind == 'square_11':
        return {(11, 11)}

    elif subkind == 'table_15':
        return {(15, 2), (15,3), (15, 4), (15,5), (15, 6)}

    elif subkind == 'table_25':
        return {(25, 2), (25,3), (25, 4), (25,5), (25, 6)}

    elif subkind == 'integers_10_100':
        return { (i+10, j+10) for i in range(90) for j in range(90) if i <= j }

    elif subkind == 'squares_10_100':
        return { (i+10, i+10) for i in range(90) }

    elif subkind == 'integers_10_100_for_rectangles':
        return { (i+10, j+10) for i in range(90) for j in range(90) if i < j }

    elif subkind == 'integers_10_100_diff7atleast':
        return { (i+10, j+10) for i in range(90) \
                              for j in range(90) \
                              if i - j >= 7 }

    elif subkind == 'integers_5_20':
        return { (i+5, j+5) for i in range(15) for j in range(15) if i <= j }

    elif subkind == 'squares_5_20':
        return { (i+5, i+5) for i in range(15) }

    elif subkind == 'integers_5_20_for_rectangles':
        return { (i+5, j+5) for i in range(15) for j in range(15) if i < j }

    elif subkind == 'integer_3_10_decimal_3_10':
        return { (i+3, Decimal(str(j+30)) / Decimal("10")) \
                            for i in range(7) \
                            for j in range(70) \
                if Decimal(str(i+3)) <= Decimal(str(j+30)) / Decimal("10") }

    elif subkind == 'integer_3_10_decimal_3_10_for_rectangles':
        return { (i+3, Decimal(str(j+30)) / Decimal("10")) \
                            for i in range(7) \
                            for j in range(70) \
                if Decimal(str(i+3)) < Decimal(str(j+30)) / Decimal("10") }

    elif subkind == 'integers_10_100_for_sums_diffs':
        return set(random.sample({ (i+10, j+10) for i in range(90) \
                                                for j in range(90) \
                                                if i < j }, 100))

    elif subkind == 'decimals_0_20_1':
        return { (Decimal(str(i/10)), Decimal(str(j/10))) for (i, j) in \
                    random.sample({ (i, j) for i in range(200) \
                                           for j in range (200) if i < j },
                                  100)}

    elif subkind == 'decimal_and_10_100_1000_for_multi':
        box_10_100_1000 = [10, 100, 1000]

        result = set()

        for n in range(20):
            if not box_10_100_1000:
                box_10_100_1000 = [10, 100, 1000]

            chosen_10_100_1000 = box_10_100_1000.pop()

            ranks_scale = list(RANKS[2:])
            width = randomly.pop([1, 2, 3], weighted_table=[0.14, 0.63, 0.33])

            start_rank = randomly.pop([n for n in range(len(ranks_scale))])

            result |= {(chosen_10_100_1000,
                        generate_decimal(width, ranks_scale, start_rank))}

        return result

    elif subkind == 'decimal_and_10_100_1000_for_divi':
        box_10_100_1000 = [10, 100, 1000]

        result = set()

        for n in range(20):
            if not box_10_100_1000:
                box_10_100_1000 = [10, 100, 1000]

            chosen_10_100_1000 = box_10_100_1000.pop()

            ranks_scale = list(RANKS[2:])
            width = randomly.pop([1, 2, 3], weighted_table=[0.14, 0.63, 0.33])

            wt = {10: [0.2, 0.2, 0.2, 0.2, 0.2],
                  100: [0.25, 0.25, 0.25, 0.25, 0],
                  1000: [0.34, 0.33, 0.33, 0, 0]}

            start_rank = randomly.pop([n for n in range(len(ranks_scale))],
                                      weighted_table=wt[chosen_10_100_1000])

            result |= {(chosen_10_100_1000,
                        generate_decimal(width, ranks_scale, start_rank))}

        return result

    elif subkind == 'decimal_and_one_digit_for_multi':
        box = [Decimal('0.1'), Decimal('0.01'), Decimal('0.001')]

        result = set()

        for n in range(20):
            if not box:
                box = [Decimal('0.1'), Decimal('0.01'), Decimal('0.001')]

            chosen = box.pop()

            ranks_scale = list()

            if chosen == Decimal('0.1'):
                ranks_scale = list(RANKS[:-1])
            elif chosen == Decimal('0.01'):
                ranks_scale = list(RANKS[:-2])
            elif chosen == Decimal('0.001'):
                ranks_scale = list(RANKS[:-3])

            width = randomly.pop([1, 2, 3, 4],
                                 weighted_table=[0.14, 0.43, 0.33, 0.2])

            start_rank = randomly.pop([n for n in range(len(ranks_scale))])

            result |= {(chosen,
                        generate_decimal(width, ranks_scale, start_rank))}

        return result

    elif subkind == 'decimal_and_one_digit_for_divi':
        box = [Decimal('0.1'), Decimal('0.01'), Decimal('0.001')]

        result = set()

        for n in range(20):
            if not box:
                box = [Decimal('0.1'), Decimal('0.01'), Decimal('0.001')]

            chosen = box.pop()

            ranks_scale = list()

            if chosen == Decimal('0.1') or chosen == Decimal('0.01'):
                ranks_scale = list(RANKS)
            elif chosen == Decimal('0.001'):
                ranks_scale = list(RANKS[1:])

            width = randomly.pop([1, 2, 3, 4],
                                 weighted_table=[0.14, 0.43, 0.33, 0.2])

            start_rank = randomly.pop([n for n in range(len(ranks_scale))])

            result |= {(chosen,
                        generate_decimal(width, ranks_scale, start_rank))}

        return result

    elif subkind == 'int_irreducible_frac':
        result = set()
        for k in [i+2 for i in range(18)]:
            result |= {(k, Fraction((n, k))) for n in coprime_generator(k)}
        return result

    elif subkind == 'rank_word':
        return {(elt,) for elt in RANKS}

    elif subkind == 'bypass':
        return set()

    else:
        raise error.OutOfRangeArgument(subkind,
                                       "'" \
                                       + " ,".join(AVAILABLE_Q_SUBKIND_VALUES) \
                                       + "'")




# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Q_MentalCalculation
# @brief Creates one whole tabular full of questions + answers
class Q_MentalCalculation(Q_Structure):


    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor.
    #   @param embedded_machine The machine to be used
    #   @param **options Any options
    #   @return One instance of question.Q_MentalCalculation
    def __init__(self, embedded_machine, q_kind,
                 q_options, **options):

        self.derived = True

        options.update(q_options)

        # The call to the mother class __init__() method will set the
        # fields matching optional arguments which are so far:
        # self.q_kind, self.q_subkind
        # plus self.machine, self.options (modified)
        Q_Structure.__init__(self, embedded_machine,
                             q_kind, None,
                             q_subkind='bypass', **options)
        # The purpose of this next line is to get the possibly modified
        # value of **options
        options = self.options

        numbers_to_use = options['numbers_to_use']
        del options['numbers_to_use']

        # module
        m = MODULES[self.q_kind].sub_object(embedded_machine,
                                            numbers_to_use,
                                            **options)

        self.q_text = m.q(embedded_machine, **options)
        self.q_answer = m.a(embedded_machine, **options)
        if hasattr(m, 'h'):
            self.q_hint = m.h(embedded_machine, **options)
        else:
            self.q_hint = ""










    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the text of the question as a str
    def text_to_str(self):
        return self.q_text








    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the answer of the question as a str
    def answer_to_str(self):
        return self.q_answer





    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the answer of the question as a str
    def hint_to_str(self):
        return self.q_hint
