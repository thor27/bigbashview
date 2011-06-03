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

import sys
import os

import pygtk
pygtk.require('2.0')
import gtk
import webkit

from bbv.globals import *
from bbv.ui.base import BaseWindow

class Window(BaseWindow):
    def __init__(self):
        raise NotImplementedError
        self.window = gtk.Window()
        self.webview = webkit.WebView()
        self.window.add(self.webview)
        self.webview.show()
        self.webview.connect("title_changed", self.title_changed)
        self.webview.connect("link_clicked", self.link_clicked)
    
    def run(self):
        gtk.main()
        return 0
    
    def set_size(self, width, height):
        if width<=0:
            width=640
        if height<=0:
            height=480
        
        self.window.resize(width, height)
    
    def show(self, *args):
        self.window.show()
    
    def load_url(self, url):
        self.webview.open(url)
        print url
        self.url_verify(url)
    
    def set_icon(self, *args):
        pass
    
    def title_changed(self, widget, frame, title):
        self.window.set_title(title)
    
    def link_clicked(self, *args):
        print args
    
    def url_verify(self, url):
        
        if url and url.endswith(".sh"):
            self.BashLoaded = True
            sys_var=self.config_tool_variables()
            sys_var_list="plist=\""
            parameters=""
            #for parameter in url.queryItems():
            #    var_name="p_"+parameter[0].__str__()
            #    var_content=parameter[1].__str__()
            #    sys_var+=var_name+"=\""+var_content+"\" "
            #    sys_var_list+=var_name+","
            #    parameters+=" \"--"+parameter[0].__str__()+"\" \""+parameter[1].__str__()+"\""
            sys_var_list+="\" "
            sys_var+=sys_var_list
            
            stdout_handle = os.popen(sys_var+url.__str__()+parameters, "r")
            HTML=stdout_handle.read().decode("utf-8")
            parser = HTMLParser(HTML)
            HTML=parser.run(self)
            self.webview.load_html_string(HTML, os.path.abspath(url))
        elif file_path:
            self.webview.open(file_path)
    
    def config_tool_variables(self):
        
        
        
        sys_var = ""
        sys_var += "WINDOW_WIDTH=" + str(width) + " "
        sys_var += "WINDOW_HEIGHT=" + str(height) + " "
        
        screen = self.window.get_screen()
        width = screen.get_width()
        height = screen.get_height()
        
        sys_var += "SCREEN_WIDTH=" + str(width) + " "
        sys_var += "SCREEN_HEIGHT=" + str(height) + " "
        sys_var += "CT_PID=" + str(os.getpid()) + " "
        return sys_var
    
    def config_tool_variables(self, url):
        
        sys_vars = os.environ.copy()
        
        width, height = self.window.get_size()
        
        sys_vars["WINDOW_WIDTH"] = str(width)
        sys_vars["WINDOW_HEIGHT"] = str(height)
        
        screen = self.window.get_screen()
        width = screen.get_width()
        height = screen.get_height()
        
        sys_vars["SCREEN_WIDTH"] = str(width)
        sys_vars["SCREEN_HEIGHT"] = str(height)
        sys_vars["CT_PID"] = str(os.getpid())
        
        sys_var_list="\""
        parameters = ""
        plist = []
        
        for parameter in url.queryItems():
            var_name = "p_" + parameter[0].__str__()
            var_content = parameter[1].__str__()
            sys_vars[var_name] = var_content
            
            plist.append(var_name)
            parameters += " \"--" + parameter[0].__str__() + "\" \"" + parameter[1].__str__() + "\""
        
        sys_vars["plist"] = "\"" + ", ".join(plist) + "\" "
        
        variables={}
        variables["sys_var"]=sys_vars
        variables["parameters"]=parameters
        
        return variables