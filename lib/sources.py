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

from lib.tools.tag import classify_tag, translate_int_pairs_tag
from lib.common import shared

##
#   @todo   Turn the old source ids' tags into the new ones:
#           table_2_9       ->      intpairs_2to9
#           table_4_9       ->      intpairs_4to9
#           table_N_11_50   ->      multipleofN_11to50
#           integers_10_100 ->      intpairs_10to100
#           integers_5_20   ->      intpairs_5to20
#           The ones that remain the same:
#           table_N (for N in [2, 3, ..., 9, 11, 15, 25])
#           The ones that will disappear:
#           *_for_sums_diffs:   a kwarg should be added to inform the source
#                               there's a special condition on the numbers to
#                               return
#           *_for_rectangles:   same as above
#           *_for_multi_reversed:   same as above
#           square*
#           Yet to think about: integers_10_100_diff7atleast
INT_PAIRS_IDS = ['tables_2_9', 'tables_4_9', 'table_2', 'table_3', 'table_4',
                 'table_11', 'table_15', 'table_25',
                 'table_2_11_50', 'table_3_11_50', 'table_4_11_50',
                 'integers_10_100', 'integers_5_20',
                 'integers_10_100_diff7atleast',
                 'table_2_9_for_sums_diffs',
                 'integers_10_100_for_sums_diffs',
                 'squares_2_9', 'squares_4_9', 'square_11',
                 'squares_10_100', 'squares_5_20',
                 'table_2_9_for_rectangles', 'table_4_9_for_rectangles',
                 'table_11_for_rectangles', 'integers_10_100_for_rectangles',
                 'integers_5_20_for_rectangles',
                 'table_2_9_for_multi_reversed', 'table_4_9_for_multi_reversed']

class mc_source(object):
    ##
    #   @brief  Initializer
    #def __init__(self):
    #    pass

    ##
    #   @brief  Handles the choice of the next value to return
    def next(self, source_id, **kwargs):
        if classify_tag(source_id) == 'int_pairs':
            kwargs.update(translate_int_pairs_tag(source_id))
            return shared.int_pairs_source.next(**kwargs)
        #elif classify_tag(source_id) == '...':
        #    return...

