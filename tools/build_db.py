#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2016 Nicolas Hainaux <nh.techn@gmail.com>

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

"""
This script adds new entries to the database.

It actually erases the database and builds it entirely.
It will add all entries:
- from files mini_pb_addi_direct.xml,mini_pb_divi_direct.xml,
  mini_pb_subtr_direct.xml and mini_pb_multi_direct.xml from data/wordings/,
- from all w4l.po files from locale/*/LC_MESSAGES/
- from all *_names.po files from locale/*/LC_MESSAGES/
- and all integers pairs from 2 to 199
"""

import os
import sqlite3

from mathmaker import settings
from mathmaker.lib.tools import po_file, xml_sheet
settings.init()

WORDINGS_DIR = settings.datadir + "wordings/"
WORDINGS_FILES = [WORDINGS_DIR + n + ".xml"
                  for n in ["mini_pb_addi_direct",
                            "mini_pb_divi_direct",
                            "mini_pb_subtr_direct",
                            "mini_pb_multi_direct"]]

# Existent db is deleted. A brand new empty db is created.
if os.path.isfile(settings.path.db_dist):
    os.remove(settings.path.db_dist)
open(settings.path.db_dist, 'a').close()
db = sqlite3.connect(settings.path.db_dist)

# Creation of the tables
db.execute('''CREATE TABLE w4l
          (id INTEGER PRIMARY KEY,
          language TEXT, word TEXT, drawDate INTEGER)''')
db.execute('''CREATE TABLE names
          (id INTEGER PRIMARY KEY,
          language TEXT, gender TEXT, name TEXT, drawDate INTEGER)''')
db.execute('''CREATE TABLE mini_pb_wordings
          (id INTEGER PRIMARY KEY,
          wording_context TEXT, wording TEXT,
          nb1_min INTEGER, nb1_max INTEGER, nb2_min INTEGER, nb2_max INTEGER,
          q_id TEXT, drawDate INTEGER)''')
db.execute('''CREATE TABLE int_pairs
          (id INTEGER PRIMARY KEY,
          nb1 INTEGER, nb2 INTEGER,
          multirev_locked INTEGER, drawDate INTEGER)''')

# Extract data from po(t) files and insert them into the db
for lang in next(os.walk(settings.localedir))[1]:
    settings.language = lang
    if os.path.isfile(settings.localedir + lang + "/LC_MESSAGES/w4l.po"):
        words = po_file.get_list_of('words', lang, 4)
        db_rows = list(zip([lang for _ in range(len(words))],
                           words,
                           [0 for _ in range(len(words))]))
        db.executemany(
            "INSERT INTO w4l(language, word, drawDate) VALUES(?, ?, ?)",
            db_rows)

    for gender in ["masculine", "feminine"]:
        if os.path.isfile(settings.localedir + lang
                          + "/LC_MESSAGES/" + gender + "_names.po"):
            # __
            names = po_file.get_list_of('names', lang, gender)
            db_rows = list(zip([lang for _ in range(len(names))],
                               [gender for _ in range(len(names))],
                               names,
                               [0 for _ in range(len(names))]))
            db.executemany("INSERT "
                           "INTO names(language, gender, name, drawDate) "
                           "VALUES(?, ?, ?, ?)",
                           db_rows)

# Extract data from xml files and insert them into the db
for f in WORDINGS_FILES:
    wordings = xml_sheet.get_attributes(f, "wording")
    db_rows = list(zip([w['wording_context'] for w in wordings],
                       [w['wording'] for w in wordings],
                       [w['nb1_min'] for w in wordings],
                       [w['nb1_max'] for w in wordings],
                       [w['nb2_min'] for w in wordings],
                       [w['nb2_max'] for w in wordings],
                       [w['q_id'] for w in wordings],
                       [0 for _ in range(len(wordings))]))
    db.executemany("INSERT "
                   "INTO mini_pb_wordings(wording_context, wording, "
                   "nb1_min, nb1_max, nb2_min, nb2_max, "
                   "q_id, drawDate) "
                   "VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                   db_rows)

# Insert integers pairs into the db
# Tables of 2, 3... 99
db_rows = [(i + 2, j + 2, 0, 0)
           for i in range(199)
           for j in range(199)
           if j >= i]
db.executemany("INSERT "
               "INTO int_pairs(nb1, nb2, "
               "multirev_locked, drawDate) "
               "VALUES(?, ?, ?, ?)",
               db_rows)

db.commit()
db.close()
