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

class UIUser:
    def __init__(self, app, parent=None, db=None, myuid=0, myname='', 
        external_func_user_edit=None):
        self.version = (0, 7, 8)
        self.name = 'UI User Management Module'
        self.info = '(c) Noprianto, 2009'
        self.db = db
        self.app = app
        self.parent = parent
        self.myuid = myuid
        self.myname = myname
        self.external_func_user_edit = external_func_user_edit
        
        self.vbox = gtk.VBox()
        self.width = self.app.main_win_width
        self.height = self.app.main_win_height 
    
    def create_ui(self):
        #search
        lbl_search_uname = gtk.Label('User name')
        self.ent_search_uname = gtk.Entry()
        lbl_search_rname = gtk.Label('Real name')
        self.ent_search_rname = gtk.Entry()
        self.combo_search = gtk.combo_box_new_text()
        self.combo_search.append_text('OR')
        self.combo_search.append_text('AND')
        self.combo_search.set_active(0)
        btn_search_do = gtk.Button(stock=gtk.STOCK_FIND)
        btn_search_do.connect('clicked', self.user_search)
        btn_search_clear = gtk.Button(stock=gtk.STOCK_CLEAR)
        btn_search_clear.connect('clicked', self.user_search_clear)
        hb_search = gtk.HBox()
        hb_search.pack_start(lbl_search_uname, padding=4,
            expand=False)
        hb_search.pack_start(self.ent_search_uname, padding=4)
        hb_search.pack_start(lbl_search_rname, padding=4,
            expand=False)
        hb_search.pack_start(self.ent_search_rname, padding=4)
        hb_search.pack_start(self.combo_search, padding=4,
            expand=False)
        hb_search.pack_start(btn_search_do, padding=4,
            expand=False)
        hb_search.pack_start(btn_search_clear, padding=4,
            expand=False)
        self.vbox.pack_start(hb_search, padding=10, expand=False)
        #
        #
        scrollw_main = gtk.ScrolledWindow()
        scrollw_main.set_policy(gtk.POLICY_AUTOMATIC,
            gtk.POLICY_AUTOMATIC)
        self.lstore_main = gtk.ListStore(str, str, str, str)
        self.trview_main = gtk.TreeView(self.lstore_main)
        self.trview_main.get_selection().set_mode(
            gtk.SELECTION_MULTIPLE)
        #
        trvcol_main_id = gtk.TreeViewColumn('ID')
        trvcol_main_id.set_min_width(80)
        cell_main_id = gtk.CellRendererText()
        trvcol_main_id.pack_start(cell_main_id, True)
        trvcol_main_id.set_attributes(cell_main_id,
            text=0)
        trvcol_main_uname = gtk.TreeViewColumn('User Name')
        trvcol_main_uname.set_min_width(140)
        cell_main_uname = gtk.CellRendererText()
        trvcol_main_uname.pack_start(cell_main_uname, True)
        trvcol_main_uname.set_attributes(cell_main_uname,
            text=1)
        trvcol_main_rname = gtk.TreeViewColumn('Real Name')
        trvcol_main_rname.set_min_width(240)
        cell_main_rname = gtk.CellRendererText()
        trvcol_main_rname.pack_start(cell_main_rname, True)
        trvcol_main_rname.set_attributes(cell_main_rname,
            text=2)
        trvcol_main_group = gtk.TreeViewColumn('Group')
        trvcol_main_group.set_min_width(140)
        cell_main_group = gtk.CellRendererText()
        trvcol_main_group.pack_start(cell_main_group, True)
        trvcol_main_group.set_attributes(cell_main_group,
            text=3)
        #
        self.trview_main.append_column(trvcol_main_id)
        self.trview_main.append_column(trvcol_main_uname)
        self.trview_main.append_column(trvcol_main_rname)
        self.trview_main.append_column(trvcol_main_group)
        self.trview_main.set_search_column(1)
        scrollw_main.add(self.trview_main)
        self.vbox.pack_start(scrollw_main)
        #
        self.lbl_main_count = gtk.Label()
        self.lbl_main_count.set_alignment(0.005, 0.5)
        self.vbox.pack_start(self.lbl_main_count, expand=False, 
            padding=10)
        #
        #
        btn_groupedit = gtk.Button('_Group Editor')
        img_groupedit = gtk.Image()
        img_groupedit.set_from_stock(gtk.STOCK_EDIT, 
            gtk.ICON_SIZE_BUTTON)
        btn_groupedit.set_image(img_groupedit)
        btn_groupedit.connect('clicked', self.group_edit)
        btn_new = gtk.Button(stock=gtk.STOCK_NEW)
        btn_new.connect('clicked', self.user_new)
        btn_edit = gtk.Button(stock=gtk.STOCK_EDIT)
        btn_edit.connect('clicked', self.user_edit)
        btn_del = gtk.Button(stock=gtk.STOCK_DELETE)
        btn_del.connect('clicked', self.user_delete)
        btn_refresh = gtk.Button(stock=gtk.STOCK_REFRESH)
        btn_refresh.connect('clicked', self.user_refresh)                        
        btnbox = gtk.HButtonBox()
        btnbox.set_layout(gtk.BUTTONBOX_END)
        btnbox.pack_start(btn_groupedit)
        btnbox.pack_start(btn_new)
        btnbox.pack_start(btn_edit)
        btnbox.pack_start(btn_del)
        btnbox.pack_start(btn_refresh)
        btnbox.set_spacing(10)
        #
        hb_action = gtk.HBox()
        hb_action.pack_start(btnbox, padding=10)
        self.vbox.pack_start(hb_action, expand=False, 
            padding=10)
        #
        return self.vbox

    def get_users(self, query=''):
        ret = []
        if query:
            q = query
        else:
            q = '''
            select id, user_name, real_name, gid, password from ms_users order by user_name
            '''
        a = ()
        r = self.db.query(q, a, self.app.database)
        if r[0] == 0:
            ret = r[1]
        return ret
    
    def get_user(self, id):
        ret = []
        users = self.get_users()
        for u in users:
            if u[0] == id:
                ret = u
                break
        #
        return ret
        

    def get_user_id(self, user):
        ret = 0
        users = self.get_users()
        for u in users:
            if u[1] == user:
                ret = u[0]
                break
        #
        return ret

    def get_user_group(self, user):
        ret = 0
        users = self.get_users()
        for u in users:
            if u[1] == user:
                ret = u[3]
                break
        #
        return ret
        
    def get_group_resources(self, group):
        ret = []
        q = '''
        select resources from ms_groups where group_name=?
        '''
        a = (group,)
        r = self.db.query(q, a, self.app.database)
        if r[0] == 0:
            try:
                res = r[1][0][0]
                if res:
                    ret = res.split(',')
                    ret.sort()
            except:
                ret = []
        return ret
    
    def get_groups(self):
        ret = []
        q = '''
        select id, group_name, resources from ms_groups order by group_name
        '''
        a = ()
        r = self.db.query(q, a, self.app.database)
        if r[0] == 0:
            ret = r[1]
        return ret

    def get_group_id(self, group):
        ret = 0
        groups = self.get_groups()
        for g in groups:
            if g[1] == group:
                ret = g[0]
                break
        #
        return ret

    def get_group_name(self, gid):
        ret = ''
        groups = self.get_groups()
        for g in groups:
            if g[0] == gid:
                ret = g[1]
                break
        #
        return ret
        
    def get_group_members(self, group):
        ret = []
        gid = self.get_group_id(group)
        q = '''
        select * from ms_users where gid=? order by user_name
        '''
        a = (gid,)
        r = self.db.query(q, a, self.app.database)
        if r[0] == 0:
            ret = r[1]
        return ret        
    
    def draw_users(self, query=''):
        self.lstore_main.clear()
        users = self.get_users(query)
        for u in users:
            id = u[0]
            uname = u[1]
            rname = u[2]
            gid = u[3]
            group = self.get_group_name(gid)
            temp = (id, uname, rname, group)
            self.lstore_main.append(temp)
        #
        msg = 'User count: %d' %(len(users))
        self.lbl_main_count.set_text(msg)        
        
    def reset_ui(self):
        self.user_search_clear(widget=None)
    
    def user_search(self, widget):
        uname = self.ent_search_uname.get_text().strip()
        rname = self.ent_search_rname.get_text().strip()
        rule = self.combo_search.get_active()
        
        #no input, quit
        if not uname and not rname:
            self.user_search_clear(widget=None)
            return
        #
        rule_str = 'OR'
        if rule == 1:
            rule_str = 'AND'
        #
        uname_add = ''
        if uname:
            uname_add = "user_name like '%%%s%%'" %(uname)
            if rname:
                uname_add += ' %s ' %(rule_str)
        rname_add = ''
        if rname:
            rname_add = "real_name like '%%%s%%'" %(rname)
        
        query = '''
        select * from ms_users where %s %s order by user_name
        ''' %(uname_add, rname_add)
        
        #
        self.draw_users(query=query.strip())
        #

    def user_search_clear(self, widget):
        self.ent_search_uname.set_text('')
        self.ent_search_rname.set_text('')
        self.combo_search.set_active(0)
        self.draw_users()
        
    def user_new(self, widget):
        d = gtk.Dialog('New User', self.parent, gtk.DIALOG_MODAL,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        d.set_size_request(self.app.main_win_width - 100, -1)

        tbl_user = gtk.Table(4, 3)        
        #
        ent_uname = gtk.Entry()
        lbl_uname = gtk.Label('User Name')
        lbl_uname.set_alignment(0, 0.5)
        tbl_user.attach(lbl_uname, 0, 1, 0, 1, xpadding=8, ypadding=8)
        tbl_user.attach(ent_uname, 1, 3, 0, 1, xpadding=8, ypadding=8)
        #
        ent_rname = gtk.Entry()
        lbl_rname = gtk.Label('Real Name')
        lbl_rname.set_alignment(0, 0.5)
        tbl_user.attach(lbl_rname, 0, 1, 1, 2, xpadding=8, ypadding=8)
        tbl_user.attach(ent_rname, 1, 3, 1, 2, xpadding=8, ypadding=8)
        #
        ent_passwd = gtk.Entry()
        lbl_passwd = gtk.Label('Password')
        lbl_passwd.set_alignment(0, 0.5)
        tbl_user.attach(lbl_passwd, 0, 1, 2, 3, xpadding=8, ypadding=8)
        tbl_user.attach(ent_passwd, 1, 3, 2, 3, xpadding=8, ypadding=8)
        #
        combo_group = gtk.combo_box_new_text()
        self.group_populate_groups(combo=combo_group)
        lbl_group = gtk.Label('Group')
        lbl_group.set_alignment(0, 0.5)
        tbl_user.attach(lbl_group, 0, 1, 3, 4, xpadding=8, ypadding=8)
        tbl_user.attach(combo_group, 1, 3, 3, 4, xpadding=8, ypadding=8)
        #
        d.vbox.pack_start(tbl_user)
        d.vbox.show_all()
        #
        ret = d.run()
        d.hide()
        
        if ret == gtk.RESPONSE_ACCEPT:
            uname = ent_uname.get_text().strip()
            rname = ent_rname.get_text().strip()
            passwd = ent_passwd.get_text().strip()
            passwd_md5 = md5.new(passwd).hexdigest()
            group = combo_group.get_active_text()
            gid = 0
            if group:
                gid = self.get_group_id(group)
            
            if not uname:
                msg = 'User Name could not be left blank'
                gtkutils.error(parent=self.parent, message=msg, 
                    title='Error')
            else:
                found = self.get_user_id(uname)
                if found:
                    msg = 'User %s already exists' %(uname)
                    gtkutils.error(message=msg, parent=d, title='Error')
                else:
                    q = '''
                    insert into ms_users(user_name, real_name, gid, password)
                    values(?,?,?,?)    
                    '''
                    a = (uname, rname, gid, passwd_md5)
                    r = self.db.query(q, a, self.app.database)
                    if r[0] != 0:
                        msg = r[1]
                        dialog = gtkutils.error
                        dialog(title='Error', message=msg, parent=d)
                    #
                    self.draw_users()
        #
        d.destroy()

    def user_edit(self, widget):
        selection = self.trview_main.get_selection()
        model, selected = selection.get_selected_rows()
        iters = [model.get_iter(path) for path in selected]
        if iters:
            iter = iters[0]
            id = int(model.get_value(iter, 0))
            user = self.get_user(id)
            #
            d = gtk.Dialog('Edit User', self.parent, gtk.DIALOG_MODAL,
                (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                    gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
            d.set_size_request(self.app.main_win_width - 100, -1)

            tbl_user = gtk.Table(4, 3)        
            #
            ent_uname = gtk.Entry()
            ent_uname.set_text(user[1])
            lbl_uname = gtk.Label('User Name')
            lbl_uname.set_alignment(0, 0.5)
            tbl_user.attach(lbl_uname, 0, 1, 0, 1, xpadding=8, ypadding=8)
            tbl_user.attach(ent_uname, 1, 3, 0, 1, xpadding=8, ypadding=8)
            #
            ent_rname = gtk.Entry()
            ent_rname.set_text(user[2])
            lbl_rname = gtk.Label('Real Name')
            lbl_rname.set_alignment(0, 0.5)
            tbl_user.attach(lbl_rname, 0, 1, 1, 2, xpadding=8, ypadding=8)
            tbl_user.attach(ent_rname, 1, 3, 1, 2, xpadding=8, ypadding=8)
            #
            ent_passwd = gtk.Entry()
            lbl_passwd = gtk.Label('Password (enter to change)')
            lbl_passwd.set_alignment(0, 0.5)
            tbl_user.attach(lbl_passwd, 0, 1, 2, 3, xpadding=8, ypadding=8)
            tbl_user.attach(ent_passwd, 1, 3, 2, 3, xpadding=8, ypadding=8)
            #
            combo_group = gtk.combo_box_new_text()
            group = self.get_group_name(user[3])
            self.group_populate_groups(combo=combo_group, active=group)
            lbl_group = gtk.Label('Group')
            lbl_group.set_alignment(0, 0.5)
            tbl_user.attach(lbl_group, 0, 1, 3, 4, xpadding=8, ypadding=8)
            tbl_user.attach(combo_group, 1, 3, 3, 4, xpadding=8, ypadding=8)
            #
            d.vbox.pack_start(tbl_user)
            d.vbox.show_all()
            #
            ret = d.run()
            d.hide()
            
            if ret == gtk.RESPONSE_ACCEPT:
                uname = ent_uname.get_text().strip()
                rname = ent_rname.get_text().strip()
                passwd = ent_passwd.get_text().strip()
                passwd_md5 = md5.new(passwd).hexdigest()
                group = combo_group.get_active_text()
                gid = 0
                if group:
                    gid = self.get_group_id(group)
                
                if not uname:
                    msg = 'User Name could not be left blank'
                    gtkutils.error(parent=self.parent, message=msg, 
                        title='Error')
                else:
                    found = self.get_user_id(uname)
                    if found and uname != user[1]:
                        msg = 'User %s already exists' %(uname)
                        gtkutils.error(message=msg, parent=d, title='Error')
                    else:
                        if passwd:
                            q = '''
                            update ms_users set user_name=?, real_name=?, gid=?, password=? 
                            where id=?
                            '''
                            a = (uname, rname, gid, passwd_md5, id)
                        else:
                            q = '''
                            update ms_users set user_name=?, real_name=?, gid=?
                            where id=?
                            '''
                            a = (uname, rname, gid, id)
                        r = self.db.query(q, a, self.app.database)
                        if r[0] != 0:
                            msg = r[1]
                            dialog = gtkutils.error
                            dialog(title='Error', message=msg, parent=d)
                        #
                        self.draw_users()
            #
            #call external function when supplied
            #and when current user information is changed
            #act as bridge between status bar module
            #and user module
            if self.myuid == id:
                if self.external_func_user_edit:
                        self.external_func_user_edit(uname)
            d.destroy()
                

    def user_delete(self, widget):
        selection = self.trview_main.get_selection()
        model, selected = selection.get_selected_rows()
        iters = [model.get_iter(path) for path in selected]
        if iters:
            ids = [int(model.get_value(iter, 0)) for iter in iters]
            names = [model.get_value(iter, 1) for iter in iters]
            
            msg3 = '\n'
            if self.myuid in ids:
                try:
                    ids.remove(self.myuid)
                    names.remove(self.myname)
                except:
                    pass
                msg3 += '\nWarning: You can not delete yourself (removed from list).'
            
            if 1 in ids:
                try:
                    ids.remove(1)
                    uid1 = self.get_group(id=1)
                    names.remove(uid1[0][1])
                except:
                    pass
                msg3 += '\nWarning: You can not delete user with uid 1.'

            count = len(ids)
            info_delete_str = '\n'.join(names)
            #
            if count > 0:
                msg = 'Are you sure you want to '
                msg += 'delete %d names(s)?' %(count)
                msg2 = 'Selected user(s):\n' + info_delete_str
                msg2 += '\n\nAll corresponding data will also be deleted.'
                msg2 += '\nThis action can not be undone.'
                msg2 += msg3
                
                ok = gtkutils.confirm(title='Please confirm', 
                    message=msg, message2=msg2, parent=self.parent,
                    buttons=gtk.BUTTONS_YES_NO)

                #if yes,
                if ok == gtk.RESPONSE_YES:
                    q = []
                    for id in ids:
                        query = 'delete from ms_users where id=?'
                        args = (id,)
                        temp = (query, args)
                        q.append(temp)
                    r = self.db.query_transact(q, self.app.database)
                    if r[0] != 0:
                        msg = r[1]
                        dialog = gtkutils.error
                        dialog(title='Error', message=msg, parent=self.parent)
                    #
                    self.draw_users()


    def user_refresh(self, widget):
        self.draw_users()
    
    def group_edit_get_res(self, combo):
        group = combo.get_active_text()
        model_res = self.trview_res.get_model()
        model_res.clear()
        self.lbl_group_members.set_text('')
        if group:
            res = self.get_group_resources(group)
            resall = self.app.resource_all
            resall.sort()
            ent = []
            for ra in resall:
                if ra in res:
                    found=True
                else:
                    found=False
                temp = (found, ra)
                ent.append(temp)
            #
            for e in ent:
                model_res.append(e)
            #
            #
            members = self.get_group_members(group)
            members_info = 'Member count: %d' %(len(members))
            self.lbl_group_members.set_text(members_info)
            
    def group_edit_chk_toggle(self, widget, path):
        model = self.trview_res.get_model()
        iter = model.get_iter(path)
        if iter:
            active = not model.get_value(iter, 0)
            model.set_value(iter, 0, active)
        #

    def group_populate_groups(self, combo, active=''):
        groups = self.get_groups()
        groups_name = [x[1] for x in groups]
        #
        model = combo.get_model()
        model.clear()
        #
        combo.append_text('')
        i = 1
        activeindex = 0
        for g in groups_name:
            combo.append_text(g)
            if g == active:
                activeindex = i
            i += 1
        if active:
            combo.set_active(activeindex)
        else:
            combo.set_active(0)

    def group_rename(self, widget):
        group = self.combo_grp.get_active_text()
        if group:
            newgroup = gtkutils.input(title='Rename Group', label='New group name',
            parent=self.group_edit_dialog, default=group).strip().upper()
            if newgroup:
                groups = self.get_groups()
                found=False
                for g in groups:
                    if newgroup == g[1] and newgroup!=group:
                        found=True
                        break
                #
                if found:
                    msg = 'Group %s already exists' %(newgroup)
                    gtkutils.error(title='Error', message=msg, 
                        parent=self.parent)
                else:
                    q = '''
                    update ms_groups set group_name=? where group_name=?
                    '''
                    a = (newgroup, group)
                    r = self.db.query(q, a, self.app.database)
                    if r[0] != 0:
                        msg = r[1]
                        dialog = gtkutils.error
                        dialog(title='Error', message=msg, parent=self.group_edit_dialog)
                    else:
                        self.group_populate_groups(combo=self.combo_grp, active=newgroup)
                    

    def group_new(self, widget):
        group = gtkutils.input(title='New Group', label='Group name',
            parent=self.group_edit_dialog).strip().upper()
        if group:
            groups = self.get_groups()
            found=self.get_group_id(group)
            #
            if found:
                msg = 'Group %s already exists' %(group)
                gtkutils.error(title='Error', message=msg, 
                    parent=self.parent)
            else:
                q = '''
                insert into ms_groups(group_name, resources)
                values(?,?)
                '''
                a = (group, '')
                r = self.db.query(q, a, self.app.database)
                if r[0] != 0:
                    msg = r[1]
                    dialog = gtkutils.error
                    dialog(title='Error', message=msg, parent=self.group_edit_dialog)
                else:
                    self.group_populate_groups(active=group, combo=self.combo_grp)
                
                
    
    def group_delete(self, widget):
        group = self.combo_grp.get_active_text()
        if group:
            gid = self.get_group_id(group)
            members = self.get_group_members(group)
            members_count = len(members)
            if members_count:
                msg = '''Group has %d member(s).\nAre you sure you want to delete group %s?\nAll users in this group will lose it's group information.''' %(
                members_count, group)
            else:
                msg = '''Are you sure you want to delete group %s?''' %(group)
            ok = gtkutils.confirm(title='Please confirm', message=msg, 
                parent=self.group_edit_dialog, buttons=gtk.BUTTONS_YES_NO)
            if ok == gtk.RESPONSE_YES:
                q1 = '''
                update ms_users set gid=0 where gid=?
                '''
                a1 = (gid,)
                q2 = '''
                delete from ms_groups where id=?
                '''
                a2 = (gid,)
                q = ((q1, a1), (q2, a2))
                r = self.db.query_transact(q, self.app.database)
                if r[0] == 0:
                    msg = 'Group %s has been deleted successfully' %(group)
                    dialog = gtkutils.info
                else:
                    msg = r[1]
                    dialog = gtkutils.error
                dialog(title='Result', message=msg, parent=self.group_edit_dialog)
                #
                self.group_populate_groups(combo=self.combo_grp)
                self.combo_grp.popup()
                
                
        
    
    def group_save(self, widget):
        group = self.combo_grp.get_active_text()
        if group:
            gid = self.get_group_id(group)
            resall = []
            model = self.trview_res.get_model()
            iter = model.get_iter_first()
            while iter:
                temp = (model.get_value(iter, 0), 
                        model.get_value(iter, 1))
                resall.append(temp)
                iter = model.iter_next(iter)
            real_resall = ','.join([x[1] for x in resall if x[0]])
            #
            q = '''
            update ms_groups set resources=? where id=?
            '''
            a = (real_resall, gid)
            r = self.db.query(q, a, self.app.database)
            if r[0] == 0:
                msg = 'Settings for group %s has been saved successfully' %(group)
                dialog = gtkutils.info
            else:
                msg = r[1]
                dialog = gtkutils.error
            dialog(title='Result', message=msg, parent=self.group_edit_dialog)
            #
                
            
    
    def group_edit(self, widget):
        self.group_edit_dialog = gtk.Dialog('Group Editor', 
            self.parent, gtk.DIALOG_MODAL,
            (gtk.STOCK_CLOSE, gtk.RESPONSE_ACCEPT))
        self.group_edit_dialog.set_size_request(
            self.width - 100, self.height - 100)
        #        
        hbox = gtk.HBox()
        vbox = gtk.VBox()
        #
        self.combo_grp = gtk.combo_box_new_text()
        self.group_populate_groups(combo=self.combo_grp)
        #
        lstore_res = gtk.ListStore(bool, str)
        self.trview_res = gtk.TreeView(lstore_res)
        trvcol_res_chk = gtk.TreeViewColumn('Select')
        trvcol_res_chk.set_min_width(60)
        trvcol_res_name = gtk.TreeViewColumn('Resource')
        trvcol_res_name.set_min_width(120)
        cell_res_chk = gtk.CellRendererToggle()
        cell_res_chk.set_property('activatable', True)
        cell_res_chk.connect('toggled', self.group_edit_chk_toggle)
        cell_res_name = gtk.CellRendererText()
        trvcol_res_chk.pack_start(cell_res_chk, True)
        trvcol_res_chk.set_attributes(cell_res_chk, active=0)
        self.trview_res.append_column(trvcol_res_chk)
        trvcol_res_name.pack_start(cell_res_name, True)
        trvcol_res_name.set_attributes(cell_res_name, text=1)
        self.trview_res.append_column(trvcol_res_name)
        lstore_res.clear()
        scrollw_res = gtk.ScrolledWindow()
        scrollw_res.set_policy(gtk.POLICY_AUTOMATIC,
            gtk.POLICY_AUTOMATIC)
        scrollw_res.add(self.trview_res)
        #
        vbox.pack_start(self.combo_grp, padding=4, expand=False)
        vbox.pack_start(scrollw_res, padding=4)
        #
        btnbox = gtk.VButtonBox()
        btnbox.set_spacing(10)
        btnbox.set_layout(gtk.BUTTONBOX_START)
        btn_save = gtk.Button(stock=gtk.STOCK_SAVE)
        btn_save.get_children()[0].get_children()[0].get_children()[1].set_text('Save settings')
        btn_save.connect('clicked', self.group_save)
        btn_del = gtk.Button(stock=gtk.STOCK_DELETE)
        btn_del.connect('clicked', self.group_delete)
        btn_rename = gtk.Button(stock=gtk.STOCK_EDIT)
        btn_rename.get_children()[0].get_children()[0].get_children()[1].set_text('Rename')
        btn_rename.connect('clicked', self.group_rename)
        btn_new = gtk.Button(stock=gtk.STOCK_NEW)
        btn_new.connect('clicked', self.group_new)
        btnbox.pack_start(btn_save)
        btnbox.pack_start(btn_rename)
        btnbox.pack_start(btn_del)
        btnbox.pack_start(btn_new)
        #
        self.lbl_group_members = gtk.Label()
        self.lbl_group_members.set_alignment(0.02, 0.5)
        #
        hbox.pack_start(vbox, padding=8)
        hbox.pack_start(btnbox, expand=False, padding=8)
        #
        self.combo_grp.connect('changed', self.group_edit_get_res)
        #        
        self.group_edit_dialog.vbox.pack_start(hbox, padding=4)
        self.group_edit_dialog.vbox.pack_start(self.lbl_group_members, padding=4,
            expand=False)
        self.group_edit_dialog.vbox.show_all()
        #        
        ret = self.group_edit_dialog.run()
        self.group_edit_dialog.destroy()
        #
        self.draw_users()
        return ret        
