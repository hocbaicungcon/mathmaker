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
"""Provide the function that builds the header comment from software infos."""

from mathmaker import (__software_name__, __version__,
                       __licence_info__, __contact__)
from mathmaker import __licence__, __url_info__, __url__, __copyright__


def generate(document_format, comment_symbol="% "):
    """Return the header comment for output text files."""
    hc = comment_symbol \
        + _("{document_format} document generated by {software_ref}")\
        .format(document_format=document_format,
                software_ref=__software_name__ + " " + __version__) + "\n"
    hc += comment_symbol + _(__licence_info__)\
        .format(software_ref=__software_name__,
                software_license=__licence__) + "\n"
    hc += comment_symbol + _(__url_info__)\
        .format(software_website=__url__) + "\n"
    hc += comment_symbol + "{copyright} {contact}\n\n"\
        .format(copyright=__copyright__, contact=__contact__)
    return hc
