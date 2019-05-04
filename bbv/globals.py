#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright (C) 2008 Wilson Pinto Júnior <wilson@openlanhouse.org>
#  Copyright (C) 2011 Thomaz de Oliveira dos Reis <thor27@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import os
import sys

APP_NAME = "Big Bash View"
APP_VERSION = "2.1"
PROGDIR = os.path.dirname(os.path.abspath(sys.argv[0]))

if os.path.isdir(os.sep.join((PROGDIR, ".hg"))):
    try:
        import subprocess
        po = subprocess.Popen(
            "hg heads --template '{rev}'", stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = po.communicate()
        APP_VERSION += ' (DEV. VERSION) rev %s' % stdout
    except:
        pass

# TODO: Check portability issues
DATA_DIR = os.path.expanduser("~/.bigbashview")
ICON = os.sep.join((PROGDIR, "bbv", "img", "icone.png"))


def ADDRESS(): return '127.0.0.1'


def PORT(): return 9000


COMPAT = False
