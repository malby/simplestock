#!/usr/bin/env python
#
#
#application main user interface
#
#

#(c) Noprianto <nop@tedut.com>, 2008-2009, GPL

import sys
import os
import gtk
import pygtk
pygtk.require('2.0')
import gobject
gobject.threads_init()  #for multithreading

#application
from application import Application

#another UI file
from ui_user import UIUser
from ui_product import UIProduct
from ui_password import UIPassword
from ui_about import UIAbout
from ui_statusbar import UIStatusBar
import db_sqlite3 as db

import gtkutils

class UIMain:
    def __init__(self):
        #application
        self.app = Application()
        self.db = db
        #

        #check for database existance, if not, build structure
        #
        if not os.path.exists(self.app.database) or os.path.getsize(self.app.database) == 0L:
            queries = self.app.init_db_query()
            for q in queries:
                r = self.db.query(q, (), self.app.database)
        #

        #main window
        self.win = gtk.Window()
        self.win.set_title(self.app.main_title)
        #confirm or not
        self.win.connect('delete_event', self.main_quit)
        #self.win.connect('destroy', self.main_quit, None, False)
        #

        #gunakan modul yang ada, hanya ambil satu dua fungsinya saja
        #keren!!!
        #untuk login
        dummypassword = UIPassword(app=self.app, db=self.db)
        password_validator = dummypassword.validate_login
        login_ok = gtkutils.simple_login(validator=password_validator)
        if not login_ok[0]:
            sys.exit(1)
        else:
            self.username = login_ok[1]
        del dummypassword

        #setelah login, gunakan modul user, hanya untuk get uid, gid, 
        #group, dan resources
        #keren!!!
        dummyuser = UIUser(app=self.app, db=self.db)
        self.uid = dummyuser.get_user_id(self.username)
        self.gid = dummyuser.get_user_group(self.username)
        self.group = dummyuser.get_group_name(self.gid)
        self.resources = dummyuser.get_group_resources(self.group)
        del dummyuser
        #
        
        #tabbed interface
        self.vb_tab = {} #dictionary to hold tabs
        self.nbook = gtk.Notebook()
        self.nbook.set_tab_pos(gtk.POS_TOP)
        for p in self.app.tabs:
            if p[0].upper() in self.resources:
                vb_temp = gtk.VBox()
                vb_temp.set_size_request(self.app.main_win_width, 
                    self.app.main_win_height)
                hb_temp = gtk.HBox()
                img_file = self.app.imgdir + p[1]
                img_temp = gtk.Image()
                if os.path.exists(img_file):
                    img_temp.set_from_file(img_file)
                else:
                    img_temp.set_from_stock(gtk.STOCK_NEW,
                        gtk.ICON_SIZE_LARGE_TOOLBAR)
                hb_temp.pack_start(img_temp)
                hb_temp.pack_start(gtk.Label(p[0]))
                hb_temp.show_all()
                self.nbook.append_page(vb_temp, hb_temp) 
                self.vb_tab[p[0].upper()] = vb_temp
            
        #

        #get status bar from module
        self.statusbar = UIStatusBar(self.app.date_format, 
            self.app.time_format, self.username, 1000)
        self.statusbar_ui = self.statusbar.create_ui()
        #

        #get ui from module
        if self.vb_tab.has_key('USER'):
            self.vb_user = self.vb_tab['USER']
            self.user = UIUser(app=self.app, 
                db=self.db, parent=self.win, 
                myuid=self.uid,
                myname=self.username,
                external_func_user_edit=self.statusbar.update_task)
            self.user_ui = self.user.create_ui()
            self.vb_user.pack_start(self.user_ui, expand=True)
        #

        #get ui from module
        if self.vb_tab.has_key('PRODUCT'):
            self.vb_product = self.vb_tab['PRODUCT']
            self.product = UIProduct(app=self.app, 
                db=self.db, parent=self.win, 
                myuid=self.uid,
                myname=self.username)
            self.product_ui = self.product.create_ui()
            self.vb_product.pack_start(self.product_ui, expand=True)
        #

        #get ui from module
        if self.vb_tab.has_key('CHANGE PASSWORD'):
            self.vb_password = self.vb_tab['CHANGE PASSWORD']
            self.password = UIPassword(app=self.app, 
                db=self.db, parent=self.win, 
                myuid=self.uid,
                myname=self.username)
            self.password_ui = self.password.create_ui()
            self.vb_password.pack_start(self.password_ui, expand=True)
        #

        #get ui from module
        if self.vb_tab.has_key('ABOUT'):
            self.vb_about = self.vb_tab['ABOUT']
            self.about = UIAbout(app=self.app, parent=self.win)
            self.about_ui = self.about.create_ui()
            self.vb_about.pack_start(self.about_ui, expand=True)
        #

        #main vbox
        self.vbox = gtk.VBox()
        self.vbox.pack_start(self.nbook)
        self.vbox.pack_start(self.statusbar_ui, expand=False)
        #

        #notebook signal handler, after all ui loaded
        self.nbook.connect('switch-page', self.nbook_switch_page)
        #
        
        #add main vbox, show all
        self.win.add(self.vbox)
        self.win.show_all()
        #
        
    
    def main_quit(self, widget, event=None, confirm=True):
        if confirm: #if confirmation set
            d = gtk.MessageDialog(self.win, gtk.DIALOG_MODAL,
                gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO,
                'Are you sure you want to quit?')
            d.set_title('Confirmation')
            ret = d.run()
            d.destroy()
            #
            if ret == gtk.RESPONSE_YES:
                self.main_quit(widget, event, False)
            else:
                return True
        else: # without confirmation
            gtk.main_quit()

    def nbook_switch_page(self, widget, page, page_num):
        tab = widget.get_nth_page(page_num)
        if tab:
            hb = widget.get_tab_label(tab)
            lbl = hb.get_children()[1]
            title = lbl.get_text().upper()
            if title == 'USER':
                self.user.draw_users()
            elif title == 'PRODUCT':
                self.product.draw_products()
            elif title == 'ABOUT':
                pass
            else:
                pass
