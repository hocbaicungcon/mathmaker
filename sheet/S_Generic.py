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

from .S_Structure import S_Structure
from .S_Structure import get_sheet_config, get_exercises_list

# ------------------------  lines_nb    col_widths   exercises
#SHEET_LAYOUT = { 'exc' : [ None,                    'all'
#                         ],
#                 'ans' : [ None,                    'all'
#                         ]
#               }

# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class S_Generic
# @brief This sheet will create a sheet matching the given xml file.
class S_Generic(S_Structure):





    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor
    #   @param embedded_machine The machine to be used
    #   @param **options Any options
    #   @return One instance of sheet.Generic
    def __init__(self, embedded_machine, filename, **options):
        self.derived = True

        (header,
         title,
         subtitle,
         text,
         answers_title,
         sheet_layout_type,
         font_size_offset,
         sheet_layout_unit,
         sheet_layout) = get_sheet_config(filename)

        S_Structure.__init__(self, embedded_machine, font_size_offset,
                             sheet_layout_unit, sheet_layout,
                             sheet_layout_type, **options)

        self.header = _(header) if header != "" else ""
        self.title = _(title) if title != "" else ""
        self.subtitle = _(subtitle) if subtitle != "" else ""
        self.text = _(text) if text != "" else ""
        self.answers_title = _(answers_title) if answers_title != "" else ""

        for ex in get_exercises_list(filename):
            self.exercises_list.append(ex(self.machine,
                                          filename=filename,
                                          **options))