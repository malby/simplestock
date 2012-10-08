#!/usr/bin/env python
#
#
#application user interface
#should provide at least: create_ui and reset_ui method
#  and another needed method
#also, create_ui() should return container (vbox,...)

#(c) Noprianto <nop@tedut.com>, 2008-2009, GPL


import os
import webbrowser

import gtk
import pygtk
pygtk.require('2.0')
import gobject

import gtkutils 

class UIAbout:
    def __init__(self, app, parent=None):
        self.version = (0, 1, 3)
        self.name = 'UI About Module'
        self.info = '(c) Noprianto, 2009'
        self.app = app
        self.parent = parent
        
        self.vbox = gtk.VBox()
        self.width = self.app.main_win_width
        self.height = self.app.main_win_height 
    
    def create_ui(self):
        vbox_logo = gtk.VBox()
        if os.path.exists(self.app.logofile):
            img_about = gtk.Image()
            img_about.set_from_file(self.app.logofile)
            vbox_logo.pack_start(img_about, expand=False, 
                padding=10)
        #
        pango_app_name = '''<span weight='ultrabold' font_desc='Courier 14'>%s</span>''' %(self.app.name)
        lbl_name = gtk.Label()
        lbl_name.set_markup(pango_app_name)
        lbl_name.set_alignment(0, 0.5)
        lbl_ver = gtk.Label(self.app.version_str)
        lbl_ver.set_alignment(0, 0.5)
        lbl_copy = gtk.Label(self.app.copyright_str)
        lbl_copy.set_alignment(0, 0.5)
        btn_web = gtk.Button('Visit tedut.com')
        btn_web.connect('clicked', self.go_website)
        #
        vbox_info = gtk.VBox()
        vbox_info.pack_start(lbl_name, expand=False, padding=4)
        vbox_info.pack_start(lbl_ver, expand=False, padding=4)
        vbox_info.pack_start(lbl_copy, expand=False, padding=4)
        vbox_info.pack_start(btn_web, expand=False, padding=8)
        #
        hbox = gtk.HBox()
        hbox.pack_start(vbox_logo, expand=False, padding=30)
        hbox.pack_start(vbox_info, expand=False, padding=10)
        #
        self.vbox.pack_start(hbox, padding=40)
        return self.vbox

    def reset_ui(self):
        pass
 
    def go_website(self, widget):
        webbrowser.open_new(self.app.website)
        
