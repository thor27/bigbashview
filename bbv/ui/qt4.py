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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

from bbv.globals import *
from bbv.ui.base import BaseWindow

class Window(BaseWindow):
    def __init__(self):
        self.debug=1
        self.app = QApplication(sys.argv)
        self.desktop= QApplication.desktop()
        self.web = QWebView()
        self.icon = QIcon()
        QWebSettings.setIconDatabasePath(DATA_DIR) 
        #self.web.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        
        QObject.connect(self.web, 
                        SIGNAL("titleChanged ( const QString &)"),
                        self.title_changed)
        QObject.connect(self.web, 
                        SIGNAL("iconChanged ()"),
                        self.icon_changed) 
        QObject.connect(self.web.page(), 
                        SIGNAL("windowCloseRequested ()"),
                        self.close_window)
        QObject.connect(self.web.page(), 
                        SIGNAL("geometryChangeRequested ( const QRect)"),
                        self.set_geometry)

    def config_tool_variables(self, url):
        
        sys_vars = os.environ.copy()
        sys_vars["WINDOW_WIDTH"] = str(self.web.width())
        sys_vars["WINDOW_HEIGHT"] = str(self.web.height())
        sys_vars["SCREEN_WIDTH"] = str(self.desktop.width())
        sys_vars["SCREEN_HEIGHT"] = str(self.desktop.height())
        sys_vars["CT_PID"] = str(os.getpid())
        
        sys_var_list="\""
        parameters = []
        plist = []
        
        for parameter in url.queryItems():
            var_name = "p_" + parameter[0].__str__().decode("utf-8")
            var_content = parameter[1].__str__().decode("utf-8")
            sys_vars[var_name] = var_content
            
            plist.append(var_name)
            parameters.append(" " + parameter[0].__str__() + " " + parameter[1].__str__() + "")
        
        sys_vars["plist"] = "\"" + ", ".join(plist) + "\" "
        
        variables={}
        variables["sys_var"]=sys_vars
        variables["parameters"]=parameters
        
        return variables
        
    def show(self,window_state):
        if window_state == "maximized" and not self.web.isMaximized():
            self.web.showNormal()
            self.web.showMaximized()
        elif window_state == "fullscreen" and not self.web.isFullScreen():
            self.web.showNormal()
            self.web.showFullScreen()
        elif window_state == "normal":
            self.web.showNormal()
        else:
            self.web.show()

    def run(self):
        return self.app.exec_()
                
    def set_debug(self, debuglevel):
        self.debug=debuglevel
    
    def set_geometry(self,geom ):
        self.web.setGeometry(geom)
        
    def close_window(self):
        sys.exit()
    
    def icon_changed(self):
        self.web.setWindowIcon(self.icon)
        self.web.setWindowIcon(self.web.icon())
            
    def title_changed(self, title):
        self.web.setWindowTitle(title)

    def load_url(self,url):
        self.url=QUrl.fromEncoded(url)
        self.web.setUrl(self.url)
    
    def set_icon(self,icon):
        self.icon = QIcon(QString(icon))
        self.web.setWindowIcon(self.icon)
        
    def set_size(self,width, height):
        if width<=0:
            width=640
        if height<=0:
            height=480
        
        left=(self.desktop.width()-width)/2
        top=(self.desktop.height()-height)/2
        
        self.web.setGeometry(left,top,width,height)
