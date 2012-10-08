#!/usr/bin/env python
#
#
#application user interface, status bar
#should provide at least: create_ui and reset_ui method
#  and another needed method
#also, create_ui() should return container (vbox,...)

#(c) Noprianto <nop@tedut.com>, 2008-2009, GPL

import gtk
import pygtk
pygtk.require('2.0')
import gobject
import time

class UIStatusBar:
    def __init__(self, date_format, time_format, myname, interval):
        self.version = (0, 1, 5)
        self.name = 'UI StatusBar Sample Module'
        self.info = '(c) Author, Year'
        #
        self.hbox = gtk.HBox()
        self.date_format = date_format
        self.time_format = time_format
        self.myname = myname
        self.interval = interval
    
    def create_ui(self):
        #stats
        self.statb_task = gtk.Statusbar()
        self.statb_task.set_has_resize_grip(False)
        #self.statb_task.get_children()[0].get_children()[0].set_alignment(0.5, 0.5)
        self.statb_task.set_size_request(-1, 25)
        self.statb_date = gtk.Statusbar()
        self.statb_date.set_has_resize_grip(False)
        #self.statb_date.get_children()[0].get_children()[0].set_alignment(0.5, 0.5)
        self.statb_date.set_size_request(-1, 25)
        self.statb_time = gtk.Statusbar()
        self.statb_time.set_has_resize_grip(False)
        #self.statb_time.get_children()[0].get_children()[0].set_alignment(0.5, 0.5)
        self.statb_time.set_size_request(-1, 25)
        self.hbox.pack_start(self.statb_task)
        self.hbox.pack_start(self.statb_date)
        self.hbox.pack_start(self.statb_time)
        #
        self.show_date_time()
        self.id_date_time = gobject.timeout_add(self.interval, 
            self.show_date_time)
        self.hbox.show_all()
        return self.hbox
    
    def reset_ui(self):
        gobject.source_remove(self.id_date_time)

    def show_date_time(self):
        time_str = time.strftime(self.time_format)
        date_str = time.strftime(self.date_format)
        self.statb_date.push(1, date_str)
        self.statb_time.push(1, time_str)
        self.statb_task.push(1, self.myname)
        return True
    
    def update_task(self, info):
        self.myname = info
