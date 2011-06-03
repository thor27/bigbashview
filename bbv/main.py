#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright (C) 2008 Wilson Pinto Júnior <wilson@openlanhouse.org>
#  Copyright (C) 2008  Thomaz de Oliveira dos Reis
#  Copyright (C) 2009  Bruno Goncalves Araujo
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

import sys
import os
import getopt
import re
import time

from bbv.globals import *
from bbv.server.bbv2server import run_server

class Main:
    width = -1
    height = -1
    toolkit = "auto"
    url = "./exemplo.sh"
    window_state="normal"
    icon = DEFAULT_ICON
    
    def __init__(self):
        try:
            opts, args = getopt.gnu_getopt(sys.argv[1:], 'hs:vt:w:i:', ['help', 'screen=',
                                       'version', "toolkit=", 'window_state=', 'icon=' ])

        except getopt.error, msg:
            print msg
            print 'for help use --help'
            sys.exit(2)
	
	if len(args):
	    self.url=args[0]
	
	for o, a in opts:
    
            if o in ('-h', '--help'):
                self.help()
    
            elif o in ('-v','--version'):
                print APP_NAME, APP_VERSION
                sys.exit()
            
            elif o in ('-s', '--screen'):
                args = a.split('x')
                
                if len(args) != 2:
                    self.help()
                
                for i in args:
                    if not i.isdigit():
                        self.help()
                
                self.width, self.height = args
                
                #Window Size
                self.width = int(self.width)
                self.height = int(self.height)
            
            elif o in ('-t','--toolkit'):
                if a in ("gtk2", "qt4"):
                    self.toolkit = a
                else:
                    self.toolkit = "auto"
            elif o in ('-w','--window_state'):
                if a in ("normal","maximized","fullscreen"):
                    self.window_state=a
	    elif o in ('-i','--icon'):
		if os.path.exists(a):
		    self.icon=a
	    
        #Create data folder if doesn't exists...
	if not os.path.isdir(DATA_DIR):
	    os.mkdir(DATA_DIR)
        
        #construct window
        if self.toolkit == "auto":
            try:
                from bbv.ui import qt4
                has_qt4 = True
            except ImportError:
                has_qt4 = False
            
            try:
                from bbv.ui import gtk2
                has_gtk2 = True
            except ImportError:
                has_gtk2 = False
            
            if not(has_qt4) and not(has_gtk2):
                print >> sys.stderr, ('bbv needs PyGTK or PyQt '
                                      'to run. Please install '
                                      'the latest stable version')
                sys.exit(1)
            
            elif has_qt4:
                self.window = qt4.Window()
            elif has_gtk2:
                self.window = gtk2.Window()
            
        elif self.toolkit == "qt4":
            try:
                from bbv.ui import qt4
                has_qt4 = True
            except ImportError:	
                has_qt4 = False
            
            if not has_qt4:
		from bbv.ui import qt4
                print >> sys.stderr, ('bbv needs PyQt '
                                      'to run. Please install '
                                      'the latest stable version')
                
                sys.exit(1)
            
            self.window = qt4.Window()
        
        elif self.toolkit == "gtk2":
            try:
                from bbv.ui import gtk2
                has_gtk2 = True
            except ImportError:
                has_gtk2 = False
            
            if not has_gtk2:
                print >> sys.stderr, ('bbv needs PyGTK '
                                      'to run. Please install '
                                      'the latest stable version')
                
                sys.exit(1)
            
            self.window = gtk2.Window()
	
	
    def help(self):
        print sys.argv[0], '[-h|--help] [-s|--screen=widthxheight] [-v|--version] [-t|--toolkit=[gtk2|qt4|]] [-w|--window_state=[normal|maximized|fullscreen]] [-i|--icon image] URL'
        sys.exit()
        
    def run(self):
        run_server()
        time.sleep(1)
        self.window.set_size(self.width,self.height)
        self.window.show(self.window_state)
        self.window.load_url(self.url)
        self.window.set_icon(self.icon)
        sys.exit(self.window.run())