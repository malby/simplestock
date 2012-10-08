#!/usr/bin/env python
#
#
#application user interface
#should provide at least: create_ui and reset_ui method
#  and another needed method
#also, create_ui() should return container (vbox,...)

#(c) Noprianto <nop@tedut.com>, 2008-2009, GPL


import md5

import gtk
import pygtk
pygtk.require('2.0')
import gobject

import gtkutils 

class UIPassword:
    def __init__(self, app, parent=None, db=None, myuid=0, myname=''):
        self.version = (0, 2, 5)
        self.name = 'UI Change Password Module'
        self.info = '(c) Noprianto, 2009'
        self.db = db
        self.app = app
        self.parent = parent
        self.myuid = myuid
        self.myname = myname
        
        self.vbox = gtk.VBox()
        self.width = self.app.main_win_width
        self.height = self.app.main_win_height 
    
    def create_ui(self):
        lbl_old = gtk.Label('Current Password')
        lbl_old.set_alignment(0, 0.5)
        self.ent_old = gtk.Entry()
        self.ent_old.set_visibility(False)
        lbl_new = gtk.Label('New Password')
        lbl_new.set_alignment(0, 0.5)
        self.ent_new = gtk.Entry()
        self.ent_new.set_visibility(False)
        lbl_again = gtk.Label('New Password (again)')
        lbl_again.set_alignment(0, 0.5)
        self.ent_again = gtk.Entry()
        self.ent_again.set_visibility(False)
        #
        btn_change = gtk.Button('_Change password')
        btn_change.connect('clicked', self.passwd_change)
        img_change = gtk.Image()
        img_change.set_from_stock(gtk.STOCK_EXECUTE,
            gtk.ICON_SIZE_BUTTON)
        btn_change.set_image(img_change)
        btnbox = gtk.HButtonBox()
        btnbox.set_layout(gtk.BUTTONBOX_END)
        btnbox.pack_start(btn_change)
        btnbox.set_spacing(10)
        #
        self.tbl = gtk.Table (4, 3)
        self.tbl.attach(lbl_old, 0, 1, 0, 1, 
            xpadding=8, ypadding=8)
        self.tbl.attach(self.ent_old, 1, 3, 0, 1, 
            xpadding=8, ypadding=8)
        self.tbl.attach(lbl_new, 0, 1, 1, 2, 
            xpadding=8, ypadding=8)
        self.tbl.attach(self.ent_new, 1, 3, 1, 2, 
            xpadding=8, ypadding=8)
        self.tbl.attach(lbl_again, 0, 1, 2, 3, 
            xpadding=8, ypadding=8)
        self.tbl.attach(self.ent_again, 1, 3, 2, 3, 
            xpadding=8, ypadding=8)
        self.tbl.attach(btnbox, 0, 3, 3, 4, 
            xpadding=8, ypadding=8)
        
        #
        self.vbox.pack_start(self.tbl, expand=False)
        return self.vbox

    def reset_ui(self):
        self.ent_old.set_text('')
        self.ent_new.set_text('')
        self.ent_again.set_text('')

    def validate_login(self, username, password):
        ret = False
        q = '''
        select password from ms_users where user_name=?
        '''
        a = (username,)
        r = self.db.query(q, a, self.app.database)
        if r[0] == 0:
            try:
                mypasswd = r[1][0][0]
                if password == mypasswd:
                    ret = True
            except:
                pass
        #
        return ret        

    def passwd_change(self, widget):
        ret = False
        old = self.ent_old.get_text()
        old_md5 = md5.new(old).hexdigest()
        new = self.ent_new.get_text()
        new_md5 = md5.new(new).hexdigest()
        again = self.ent_again.get_text()
        again_md5 = md5.new(again).hexdigest()
        
        if self.validate_login(self.myname, old_md5):
            #correct old password
            if new_md5 == again_md5:
                if new == '':
                    msg = 'New password could not be left blank'
                    gtkutils.error(title='Error', message=msg, parent=self.parent)
                else:
                    #change here
                    q = '''
                    update ms_users set password=? where id=?
                    '''
                    a = (new_md5, self.myuid)
                    r2 = self.db.query(q, a, self.app.database)
                    if r2[0] == 0:
                        #changed
                        msg = 'Password has been changed successfully'
                        gtkutils.info(title='Done', message=msg, parent=self.parent)
                        ret = True
                    else:
                        gtkutils.error(title='Error', message=r2[1], parent=self.parent)
            else:
                msg = 'New password mismatch'
                gtkutils.error(title='Error', message=msg, parent=self.parent)
        else:
            msg = 'Authentication failed'
            gtkutils.error(title='Error', message=msg, parent=self.parent)
        #
        if ret:
            self.reset_ui()
        #
        return ret
        
