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

# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @package question
# @brief All question objects should be "declared" here.

from . import Q_Structure

from . import Q_AlgebraExpressionReduction
from . import Q_AlgebraExpressionExpansion
from . import Q_Equation
from . import Q_Calculation
from . import Q_Factorization
from . import Q_MentalCalculation
from . import Q_RightTriangle


Q_Structure = Q_Structure.Q_Structure

Q_AlgebraExpressionReduction = \
            Q_AlgebraExpressionReduction.Q_AlgebraExpressionReduction
Q_AlgebraExpressionExpansion = \
            Q_AlgebraExpressionExpansion.Q_AlgebraExpressionExpansion
Q_Calculation = Q_Calculation.Q_Calculation
Q_Equation = Q_Equation.Q_Equation
Q_Factorization = Q_Factorization.Q_Factorization
generate_numbers = Q_MentalCalculation.generate_numbers
Q_MentalCalculation = Q_MentalCalculation.Q_MentalCalculation
Q_RightTriangle = Q_RightTriangle.Q_RightTriangle
