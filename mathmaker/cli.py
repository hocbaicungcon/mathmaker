# -*- coding: utf-8 -*-

# Copyright 2006-2015 Nicolas Hainaux <nico_h@users.sourceforge.net>

# This file is part of Mathmaker.

# Mathmaker is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

# Mathmaker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Mathmaker; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

# import time
# start_time = time.time()
import sys
import os
import argparse
import locale

from .lib import __info__, __software_name__
from . import settings
from .lib import shared
from .lib import startup_actions
from .lib import sheet
from .lib.tools.xml_sheet import get_xml_sheets_paths


def entry_point():
    settings.init()
    XML_SHEETS = get_xml_sheets_paths()
    log = settings.mainlogger
    startup_actions.check_dependencies()
    parser = argparse.ArgumentParser(description='Creates maths exercices and '
                                                 'their answers.')
    parser.add_argument('-l', '--language', action='store', dest='lang',
                        default=settings.language,
                        help='force the language of the output to LANGUAGE. '
                             'You can configure the value to be read from '
                             '~/.config/mathmaker/user_config.yaml')
    parser.add_argument('-d', '--output-directory', action='store',
                        dest='outputdir',
                        default=settings.outputdir,
                        help='where to put the possible output files, like '
                             'pictures. Default value is set to current '
                             'directory. You can change it too in '
                             '~/.config/mathmaker/user_config.yaml')
    parser.add_argument('-F', '--font', action='store',
                        dest='font',
                        default=settings.font,
                        help='The font to use. If it\'s not installed on '
                             'your system, lualatex will have then trouble '
                             'to compile the document. You can configure '
                             'a default value for the font in '
                             '~/.config/mathmaker/user_config.yaml')
    parser.add_argument('-e', '--encoding', action='store',
                        dest='encoding',
                        default=settings.encoding,
                        help='The encoding to use. Take care it\'s available '
                             ' on your system, otherwise you may have trouble '
                             'to compile the document. You can configure '
                             'a default value for the encoding in '
                             '~/.config/mathmaker/user_config.yaml')
    parser.add_argument('main_directive', metavar='[DIRECTIVE|FILE]',
                        help='this can be either a sheetname included in '
                             'mathmaker or a mathmaker xml file.')
    parser.add_argument('--version', '-v',
                        action='version',
                        version=__info__)
    args = parser.parse_args()
    startup_actions.install_gettext_translations(language=args.lang)
    # From now on, settings.language has its definitive value
    settings.outputdir = args.outputdir
    settings.font = args.font
    settings.encoding = args.encoding
    # todo: update settings.locale according to the final settings.encoding
    #       value
    locale.setlocale(locale.LC_ALL, settings.locale)
    startup_actions.check_settings_consistency()
    shared.init()

    if args.main_directive in sheet.AVAILABLE:
        sh = sheet.AVAILABLE[args.main_directive][0]()
    elif args.main_directive in XML_SHEETS:
        sh = sheet.S_Generic(filename=XML_SHEETS[args.main_directive])
    elif os.path.isfile(args.main_directive):
        sh = sheet.S_Generic(filename=args.main_directive)
    else:
        log.error(args.main_directive
                  + " is not a correct directive for " + __software_name__
                  + ", you should use any item from the following lists: "
                  + str(sorted([key for key in sheet.AVAILABLE]))
                  + str(sorted([key for key in XML_SHEETS])))
        # print("--- {sec} seconds ---"\
        #      .format(sec=round(time.time() - start_time, 3)))
        sys.exit(2)

    try:
        shared.machine.write_out(str(sh))
    except Exception:
        log.error("An exception occured during the creation of the sheet.",
                  exc_info=True)

    shared.db.commit()
    shared.db.close()
    log.info("Done.")


if __name__ == '__main__':
    entry_point()
    # print("--- {sec} seconds ---".format(sec=time.time() - start_time))