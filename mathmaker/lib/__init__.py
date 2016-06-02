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

__software_name__ = 'mathmaker'
__version__ = '0.6.1 (alpha)'
__author__ = 'Nicolas Hainaux'
__author_email__ = 'nh.techn@gmail.com'
__licence__ = 'GNU General Public License v3 or later (GPLv3+)'
__url__ = 'http://mathmaker.sourceforge.net'
__copyright__ = 'Copyright 2006-2016'
__contact__ = '{author} <{author_email}>'\
              .format(author=__author__, author_email=__author_email__)
__licence_info__ = '{software_ref} is free software. Its license is '\
                   '{software_license}.'
__url_info__ = 'Further details on {software_website}'
__info__ = '{software_name} {v}\nLicense: {l}\n{c} {contact}'\
           .format(software_name=__software_name__,
                   v=__version__, l=__licence__, c=__copyright__,
                   contact=__contact__)


# --------------------------------------------------------------------------
##
#   @brief  Turns a dictionary containing nested dictionaries into a one level
#           dictionary. Like {'a': {'a1': 3, 'a2':4}, 'b': 'data'} will
#           become {'a.a1': 3, 'a.a2': 4, 'b': 'data'}
def flat_dict(d, sep='.'):
    output = {}
    for key in d:
        if isinstance(d[key], dict):
            ud = flat_dict(d[key])
            for k in ud:
                output.update({str(key) + sep + str(k): ud[k]})
        else:
            output.update({key: d[key]})
    return output


def generate_header_comment(document_format, comment_symbol="%"):
    """Returns the header comment for output text files."""
    hc = comment_symbol + " "\
         + _("{document_format} document generated by {software_ref}")\
             .format(document_format=document_format,
                     software_ref=__software_name__ + " " + __version__) + "\n"
    hc += comment_symbol + " " + _(__licence_info__)\
                                 .format(software_ref=__software_name__,
                                         software_license=__licence__) + "\n"
    hc += comment_symbol + " " + _(__url_info__)\
                                .format(software_website=__url__) + "\n"
    hc += comment_symbol + " " + "{copyright} {contact}\n\n"\
                                 .format(copyright=__copyright__,
                                         contact=__contact__)
    return hc

