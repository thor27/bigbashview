#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright (C) 2008 Wilson Pinto Júnior <wilson@openlanhouse.org>
#  Copyright (C) 2008  Thomaz de Oliveira dos Reis
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
import os,sys

APP_NAME = "Big Bash View"
APP_VERSION = "2.0.1 (beta)"
DATA_DIR = os.path.expanduser("~/.bigbashview") # TODO: Check portability issues
DEFAULT_ICON = os.path.dirname(os.path.abspath(sys.argv[0]))+os.sep+"bbv"+os.sep+"img"+os.sep+"icone.png"
ADDRESS = lambda: '127.0.0.1'
PORT = lambda: 9000