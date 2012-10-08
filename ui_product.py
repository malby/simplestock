#!/usr/bin/env python
#
#
#application user interface
#should provide at least: create_ui and reset_ui method
#  and another needed method
#also, create_ui() should return container (vbox,...)

#(c) Noprianto <nop@tedut.com>, 2008-2009, GPL

import csv

import gtk
import pygtk
pygtk.require('2.0')
import gobject

import gtkutils 

class UIProduct:
    def __init__(self, app, parent=None, db=None, myuid=0, myname=''):
        self.version = (0, 8, 9)
        self.name = 'UI Product Management Module'
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
        #search
        lbl_search_id = gtk.Label('ID')
        self.ent_search_id = gtk.Entry()
        self.ent_search_id.set_size_request(20, -1)
        lbl_search_pname = gtk.Label('Product name')
        self.ent_search_pname = gtk.Entry()
        self.ent_search_pname.set_size_request(40, -1)
        lbl_search_price = gtk.Label('Price (expr.)')
        btn_search_price_h = gtk.Button('?')
        btn_search_price_h.connect('clicked', self.help, 'price')
        self.ent_search_price = gtk.Entry()
        self.ent_search_price.set_size_request(40, -1)
        lbl_search_stock = gtk.Label('Stock (expr.)')
        self.ent_search_stock = gtk.Entry()
        btn_search_stock_h = gtk.Button('?')
        btn_search_stock_h.connect('clicked', self.help, 'stock')
        self.ent_search_stock.set_size_request(40, -1)
        lbl_search_cat = gtk.Label('Category')
        self.combo_search_cat = gtk.combo_box_new_text()
        self.combo_search_cat.set_size_request(40, -1)
        self.combo_search = gtk.combo_box_new_text()
        self.combo_search.append_text('OR')
        self.combo_search.append_text('AND')
        self.combo_search.set_active(0)
        btn_search_do = gtk.Button(stock=gtk.STOCK_FIND)
        btn_search_do.connect('clicked', self.product_search)
        btn_search_clear = gtk.Button(stock=gtk.STOCK_CLEAR)
        btn_search_clear.connect('clicked', self.product_search_clear)
        hb_search = gtk.HBox()
        hb_search.pack_start(lbl_search_id, padding=4,
            expand=False)
        hb_search.pack_start(self.ent_search_id, padding=4)
        hb_search.pack_start(lbl_search_pname, padding=4,
            expand=False)
        hb_search.pack_start(self.ent_search_pname, padding=4)
        hb_search.pack_start(lbl_search_price, padding=4,
            expand=False)
        hb_search.pack_start(btn_search_price_h, expand=False)
        hb_search.pack_start(self.ent_search_price, padding=4)
        hb_search.pack_start(lbl_search_stock, padding=4,
            expand=False)
        hb_search.pack_start(btn_search_stock_h, expand=False)
        hb_search.pack_start(self.ent_search_stock, padding=4)
        hb_search.pack_start(lbl_search_cat, padding=4,
            expand=False)
        hb_search.pack_start(self.combo_search_cat, padding=4)
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
        self.lstore_main = gtk.ListStore(str, str, str, str, str, str, str)
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
        trvcol_main_pname = gtk.TreeViewColumn('Product Name')
        trvcol_main_pname.set_min_width(120)
        cell_main_pname = gtk.CellRendererText()
        trvcol_main_pname.pack_start(cell_main_pname, True)
        trvcol_main_pname.set_attributes(cell_main_pname,
            text=1)
        trvcol_main_cat = gtk.TreeViewColumn('Category')
        trvcol_main_cat.set_min_width(120)
        cell_main_cat = gtk.CellRendererText()
        trvcol_main_cat.pack_start(cell_main_cat, True)
        trvcol_main_cat.set_attributes(cell_main_cat,
            text=2)
        trvcol_main_price = gtk.TreeViewColumn('Price')
        trvcol_main_price.set_min_width(120)
        cell_main_price = gtk.CellRendererText()
        trvcol_main_price.pack_start(cell_main_price, True)
        trvcol_main_price.set_attributes(cell_main_price,
            text=3)
        trvcol_main_stock = gtk.TreeViewColumn('Stock')
        trvcol_main_stock.set_min_width(100)
        cell_main_stock = gtk.CellRendererText()
        trvcol_main_stock.pack_start(cell_main_stock, True)
        trvcol_main_stock.set_attributes(cell_main_stock,
            text=4)
        trvcol_main_minstock = gtk.TreeViewColumn('Min.Stock')
        trvcol_main_minstock.set_min_width(100)
        cell_main_minstock = gtk.CellRendererText()
        trvcol_main_minstock.pack_start(cell_main_minstock, True)
        trvcol_main_minstock.set_attributes(cell_main_minstock,
            text=5)
        trvcol_main_unit = gtk.TreeViewColumn('Unit')
        trvcol_main_unit.set_min_width(100)
        cell_main_unit = gtk.CellRendererText()
        trvcol_main_unit.pack_start(cell_main_unit, True)
        trvcol_main_unit.set_attributes(cell_main_unit,
            text=6)
        #
        self.trview_main.append_column(trvcol_main_id)
        self.trview_main.append_column(trvcol_main_pname)
        self.trview_main.append_column(trvcol_main_cat)
        self.trview_main.append_column(trvcol_main_price)
        self.trview_main.append_column(trvcol_main_stock)
        self.trview_main.append_column(trvcol_main_minstock)
        self.trview_main.append_column(trvcol_main_unit)
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
        btn_flow = gtk.Button('Flo_w Control')
        img_flow = gtk.Image()
        img_flow.set_from_stock(gtk.STOCK_EXECUTE, 
            gtk.ICON_SIZE_BUTTON)
        btn_flow.set_image(img_flow)
        btn_flow.connect('clicked', self.product_flow)
        btn_viewflow = gtk.Button('Flow _Report')
        img_viewflow = gtk.Image()
        img_viewflow.set_from_stock(gtk.STOCK_OPEN, 
            gtk.ICON_SIZE_BUTTON)
        btn_viewflow.set_image(img_viewflow)
        btn_viewflow.connect('clicked', self.product_view_flow)                        
        btn_catedit = gtk.Button('_Category Editor')
        img_catedit = gtk.Image()
        img_catedit.set_from_stock(gtk.STOCK_EDIT, 
            gtk.ICON_SIZE_BUTTON)
        btn_catedit.set_image(img_catedit)
        btn_catedit.connect('clicked', self.category_edit)
        btn_unitedit = gtk.Button('_Unit Editor')
        img_unitedit = gtk.Image()
        img_unitedit.set_from_stock(gtk.STOCK_EDIT, 
            gtk.ICON_SIZE_BUTTON)
        btn_unitedit.set_image(img_unitedit)
        btn_unitedit.connect('clicked', self.unit_edit)
        btn_new = gtk.Button(stock=gtk.STOCK_NEW)
        btn_new.connect('clicked', self.product_new)
        btn_edit = gtk.Button(stock=gtk.STOCK_EDIT)
        btn_edit.connect('clicked', self.product_edit)
        btn_del = gtk.Button(stock=gtk.STOCK_DELETE)
        btn_del.connect('clicked', self.product_delete)
        btn_refresh = gtk.Button(stock=gtk.STOCK_REFRESH)
        btn_refresh.connect('clicked', self.product_refresh)                        
        btn_excsv = gtk.Button('Export CS_V')
        img_excsv = gtk.Image()
        img_excsv.set_from_stock(gtk.STOCK_SAVE, 
            gtk.ICON_SIZE_BUTTON)
        btn_excsv.set_image(img_excsv)
        btn_excsv.connect('clicked', self.product_export_csv)                        
        btnbox = gtk.HButtonBox()
        btnbox.set_layout(gtk.BUTTONBOX_END)
        btnbox.set_spacing(10)
        btnbox2 = gtk.HButtonBox()
        btnbox2.set_layout(gtk.BUTTONBOX_END)
        btnbox2.set_spacing(10)
        btnbox.pack_start(btn_flow)
        btnbox.pack_start(btn_viewflow)
        btnbox.pack_start(btn_catedit)
        btnbox.pack_start(btn_unitedit)        
        btnbox2.pack_start(btn_new)
        btnbox2.pack_start(btn_edit)
        btnbox2.pack_start(btn_del)
        btnbox2.pack_start(btn_refresh)
        btnbox2.pack_start(btn_excsv)
        
        #
        hb_action = gtk.VBox()
        hb_btnbox = gtk.HBox()
        hb_btnbox.pack_start(btnbox, padding=10)
        hb_btnbox2 = gtk.HBox()
        hb_btnbox2.pack_start(btnbox2, padding=10)
        hb_action.pack_start(hb_btnbox, padding=10)
        hb_action.pack_start(hb_btnbox2, padding=10)
        self.vbox.pack_start(hb_action, expand=False, 
            padding=10)
        #
        #tip
        self.tips = gtk.Tooltips()
        self.tips.enable()
        self.tips.set_tip(self.ent_search_stock, 'Test')
        
        #
        return self.vbox

    def help(self, widget, topic):
        if topic == 'price':
            helpstr = '''
            1. You can use valid SQL operator, for example:
               >, <, =, <>, >=, <=, AND, OR.
            2. Field name: price
            3. Example:
               = 1000
               > 1000
               < 1000
               > 1000 AND price < 10000
            
            '''
        elif topic == 'stock':
            helpstr = '''
            1. You can use valid SQL operator, for example:
               >, <, =, <>, >=, <=, AND, OR.
            2. Field name: stock
            3. Min Stock field name: minstock
            4. Example:
               = 100
               > 100
               < 100
               > 100 AND stock < 200
               = minstock
               < minstock
            '''
        else:
            helpstr = 'No help topic found'
        gtkutils.tips(caption='Help', tip=helpstr, width=500, parent=self.parent)

    def get_products(self, query=''):
        ret = []
        if query:
            q = query
        else:
            q = '''
            select id, product_name, price, uid, cid, stock,minstock from ms_products order by product_name
            '''
        a = ()
        r = self.db.query(q, a, self.app.database)
        if r[0] == 0:
            ret = r[1]
        return ret
    
    def get_product(self, id):
        ret = []
        products = self.get_products()
        for u in products:
            if u[0] == id:
                ret = u
                break
        #
        return ret
        

    def get_product_id(self, product):
        ret = 0
        products = self.get_products()
        for p in products:
            if p[1] == product:
                ret = p[0]
                break
        #
        return ret

    def get_product_flow(self, id):
        ret = []
        q = '''
        select dateinfo, user, pid, flow_type, amount, note from tr_flow where pid=? order by id
        '''
        a = (id,)
        r = self.db.query(q, a, self.app.database)
        if r[0] == 0:
            ret = r[1]
        return ret
        
            
    def get_categories(self):
        ret = []
        q = '''
        select id, category_name, note from ms_categories order by category_name
        '''
        a = ()
        r = self.db.query(q, a, self.app.database)
        if r[0] == 0:
            ret = r[1]
        return ret

    def get_category_id(self, category):
        ret = 0
        categories = self.get_categories()
        for c in categories:
            if c[1] == category:
                ret = c[0]
                break
        #
        return ret

    def get_category_name(self, cid):
        ret = ''
        categories = self.get_categories()
        for c in categories:
            if c[0] == cid:
                ret = c[1]
                break
        #
        return ret

    def get_category_note(self, category):
        ret = ''
        categories = self.get_categories()
        for c in categories:
            if c[1] == category:
                ret = c[2]
                break
        #
        return ret

    def get_category_members(self, cid):
        ret = []
        products = self.get_products()
        for p in products:
            if p[4] == cid:
                ret.append(p)
        #
        return ret

    def get_units(self):
        ret = []
        q = '''
        select id, unit_name, note from ms_units order by unit_name
        '''
        a = ()
        r = self.db.query(q, a, self.app.database)
        if r[0] == 0:
            ret = r[1]
        return ret

    def get_unit_id(self, unit):
        ret = 0
        units = self.get_units()
        for u in units:
            if u[1] == unit:
                ret = u[0]
                break
        #
        return ret

    def get_unit_name(self, uid):
        ret = ''
        units = self.get_units()
        for u in units:
            if u[0] == uid:
                ret = u[1]
                break
        #
        return ret

    def get_unit_note(self, unit):
        ret = ''
        units = self.get_units()
        for u in units:
            if u[1] == unit:
                ret = u[2]
                break
        #
        return ret

    def get_unit_members(self, uid):
        ret = []
        products = self.get_products()
        for p in products:
            if p[3] == uid:
                ret.append(p)
        #
        return ret
        
    def product_export_csv(self, widget):
        d = gtk.FileChooserDialog('Select output file', self.parent,
            action=gtk.FILE_CHOOSER_ACTION_SAVE, 
            buttons=(gtk.STOCK_SAVE, gtk.RESPONSE_OK))
        d.set_select_multiple(False)
        #
        filter_csv = gtk.FileFilter()
        filter_csv.set_name('CSV File')
        filter_csv.add_pattern('*.csv')
        #
        d.add_filter(filter_csv)
        #
        res = d.run()
        d.hide()
        if res == gtk.RESPONSE_OK:
            filename = d.get_filename()
            if filename:
                ent = []
                products = self.get_products()
                title = ('ID', 'Product Name', 'Category', 
                    'Price', 'Stock', 'Min.Stock', 'Unit')
                ent.append(title)
                for p in products:
                    id = p[0]
                    pname = p[1]
                    price = p[2]
                    unit = self.get_unit_name(p[3])
                    cat = self.get_category_name(p[4])
                    stock = p[5]
                    minstock = p[6]
                    temp = (id, pname, cat, price, stock, minstock, unit)
                    ent.append(temp)
                #write
                try:
                    writer = csv.writer(open(filename, 'wb'))
                    writer.writerows(ent)
                    msg = 'Data have been successfully exported to %s' %(filename)
                    gtkutils.info(title='Done', message=msg, parent=self.parent)
                except:
                    msg = 'Failed writing to %s' %(filename)
                    gtkutils.error(title='Error', message=msg, parent=self.parent)
        #
        d.destroy()
        #
    
    def draw_products(self, query='', clear_combo=True):
        self.lstore_main.clear()
        products = self.get_products(query)
        for p in products:
            id = p[0]
            pname = p[1]
            price = p[2]
            unit = self.get_unit_name(p[3])
            cat = self.get_category_name(p[4])
            stock = p[5]
            minstock = p[6]
            temp = (id, pname, cat, price, stock, minstock, unit)
            self.lstore_main.append(temp)
        #
        msg = 'Product count: %d' %(len(products))
        self.lbl_main_count.set_text(msg)        
        #
        if clear_combo:
            self.product_populate_categories(combo=self.combo_search_cat)
        
    def reset_ui(self):
        self.product_search_clear(widget=None)
    
    def product_search(self, widget):
        id = self.ent_search_id.get_text().strip()
        pname = self.ent_search_pname.get_text().strip()
        price = self.ent_search_price.get_text().strip()
        stock = self.ent_search_stock.get_text().strip()
        cat = self.combo_search_cat.get_active_text()
        cid = self.get_category_id(cat)
        rule = self.combo_search.get_active()
        
        #no input, quit
        if (not id) and (not pname) and (not price) and (not stock) and (not cid):
            self.product_search_clear(widget=None)
            return
        #
        rule_str = 'OR'
        if rule == 1:
            rule_str = 'AND'
        #
        id_add = ''
        if id:
            id_add = "id='%s'" %(id)
            if pname or price or stock or cid>0:
                id_add += ' %s ' %(rule_str)
        pname_add = ''
        if pname:
            pname_add = " product_name like '%%%s%%'" %(pname)
            if price or stock or cid>0:
                pname_add += ' %s ' %(rule_str)
        price_add = ''
        if price:
            price_add = " price %s " %(price)
            if stock or cid>0:
                price_add += ' %s ' %(rule_str)
        stock_add = ''
        if stock:
            stock_add = " stock %s" %(stock)
            if cid>0:
                stock_add += ' %s ' %(rule_str)
        cat_add = ''
        if cid>0:
            cat_add = ' cid=%d ' %(cid)

        query = '''
        select * from ms_products where %s %s %s %s %s order by product_name
        ''' %(id_add, pname_add, price_add, stock_add, cat_add)
        
        
        #
        self.draw_products(query=query.strip(), clear_combo=False)
        #

    def product_search_clear(self, widget):
        self.ent_search_id.set_text('')
        self.ent_search_pname.set_text('')
        self.ent_search_price.set_text('')
        self.ent_search_stock.set_text('')
        self.combo_search_cat.set_active(0)
        self.combo_search.set_active(0)
        self.draw_products()

    def product_flow_get_idames_model(self):
        products = self.get_products()
        idnames = [[' - '.join((x[0],x[1], '(stock: ' + str(x[5]) + ')'))] for x in products]
        #
        model = gtk.ListStore(str)
        model.append([''])#baris kosong
        for i in idnames:
            model.append(i)
        #
        return model
    
    def product_flow_cell_edited(self, cell, path, new_text, model, col):
        iter = model.get_iter(path)
        model.set_value(iter, col, new_text)
    
    def product_flow_combo_edited(self, cellrenderertext, path, new_text, trview, col):
        model = trview.get_model()
        iter = model.get_iter(path)
        model.set_value(iter, col, new_text)
        
    def product_flow_new_entry(self, widget, trview):
        ent = ['', '', '']
        model = trview.get_model()
        model.append(ent)
        
        #dapatkan baris terakhir
        iter = model.get_iter_first()
        while iter:
            lastiter = iter #simpan sebelumnya
            iter = model.iter_next(iter) #kembalikan None kalau gak ada baris terakhir
        if not iter: 
            iter = lastiter
        #select
        selection = trview.get_selection()
        selection.select_iter(iter)
    
    def product_flow_delete_entry(self, widget, trview):
        selection = trview.get_selection()
        model, iter = selection.get_selected()
        if iter:
            #get next row
            nextiter = model.iter_next(iter)

            #remove            
            model.remove(iter)
            
            #select 
            if nextiter:
                selection.select_iter(nextiter)
    
    def product_flow_save(self, widget, combo_type, cal, trview, cell_prd):
        type = combo_type.get_active_text()
        #
        date = cal.get_date()
        date2 = '%04d/%02d/%02d' %(date[0], date[1]+1, date[2])
        #
        flows = []
        model = trview.get_model()
        iter = model.get_iter_first()
        while iter:
            idname = model.get_value(iter, 0)
            id = idname.split(' - ')[0]
            amount = model.get_value(iter, 1)
            try:
                amount2 = int(amount)
            except:
                amount2 = 0
            note = model.get_value(iter, 2)
            iter = model.iter_next(iter)
            temp = (id, amount2, note)
            flows.append(temp)
        #
        q = []
        text = ''
        count = 0
        for f in flows:
            if f[0] and f[1]:
                query = '''
                insert into tr_flow(dateinfo, user, pid, flow_type, amount, note)
                values (?,?,?,?,?,?)
                '''
                args = (date2, self.myname, f[0], type, f[1], f[2])
                temp = (query, args)
                q.append(temp)
                #
                text += '[%s] %s %s %d %s\n' %(date2, f[0], type, f[1], f[2])
                count += 1
                #
                #simpan ke stock
                if type == 'IN':
                    query = '''
                    update ms_products set stock=stock+%d where id=?
                    ''' %(f[1])
                elif type == 'OUT':
                    query = '''
                    update ms_products set stock=stock-%d where id=?
                    ''' %(f[1])
                args = (f[0],)
                temp2 = (query, args)
                q.append(temp2)
        #
        if count:
            r = self.db.query_transact(q, self.app.database)
            if r[0] == 0:
                msg = 'All transactions have been saved successfully\n\n%s' %(text)
                gtkutils.info(parent=self.parent, title='Done', message=msg)
                model.clear()
                #combo dibuat ulang dengan data terbaru
                cell_prd.set_property('model', self.product_flow_get_idames_model())
                #
                #draw ulang produk
                self.draw_products()
            else:
                gtkutils.error(parent=self.parent, title='Error', message=r[1])

    def product_view_flow(self, widget):
        selection = self.trview_main.get_selection()
        model, selected = selection.get_selected_rows()
        iters = [model.get_iter(path) for path in selected]
        if iters:
            iter = iters[0]
            id = model.get_value(iter, 0)
            #
            product = self.get_product(id)
            pname = product[1]
            stock = product[5]
            pinfo = '<b>Product</b>: %s - %s, <b>Stock</b>: %d' %(id, pname, stock)
            lbl_info = gtk.Label()
            lbl_info.set_alignment(0.01, 0.5)
            lbl_info.set_markup(pinfo)
            #
            lstore = gtk.ListStore(str, str, str, str, str)
            trview = gtk.TreeView(lstore)
            scrollw = gtk.ScrolledWindow()
            scrollw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
            scrollw.add(trview)
            trvcol_date = gtk.TreeViewColumn('Date')
            trvcol_date.set_min_width(120)
            trvcol_user = gtk.TreeViewColumn('User')
            trvcol_user.set_min_width(120)
            trvcol_flow = gtk.TreeViewColumn('Flow')
            trvcol_flow.set_min_width(120)
            trvcol_amt = gtk.TreeViewColumn('Amount')
            trvcol_amt.set_min_width(120)
            trvcol_note = gtk.TreeViewColumn('Note')
            trvcol_note.set_min_width(120)
            cell_user = gtk.CellRendererText()
            cell_date = gtk.CellRendererText()
            cell_flow = gtk.CellRendererText()
            cell_amt = gtk.CellRendererText()
            cell_note = gtk.CellRendererText()
            trvcol_date.pack_start(cell_date, True)
            trvcol_date.set_attributes(cell_date, text=0)
            trvcol_user.pack_start(cell_user, True)
            trvcol_user.set_attributes(cell_user, text=1)
            trvcol_flow.pack_start(cell_flow, True)
            trvcol_flow.set_attributes(cell_flow, text=2)
            trvcol_amt.pack_start(cell_amt, True)
            trvcol_amt.set_attributes(cell_amt, text=3)
            trvcol_note.pack_start(cell_note, True)
            trvcol_note.set_attributes(cell_note, text=4)
            trview.append_column(trvcol_date)
            trview.append_column(trvcol_user)
            trview.append_column(trvcol_flow)
            trview.append_column(trvcol_amt)
            trview.append_column(trvcol_note)
            #
            flows = self.get_product_flow(id)
            lstore.clear()
            for f in flows:
                dateinfo = f[0]
                user = f[1]
                flow_type = f[3]
                amount = f[4]
                note = f[5]
                ent = [dateinfo, user, flow_type, amount, note]
                lstore.append(ent)
            #
            d = gtk.Dialog('Flow Report', 
                self.parent, gtk.DIALOG_MODAL,
                (gtk.STOCK_CLOSE, gtk.RESPONSE_ACCEPT))
            d.set_size_request(
                self.width - 100, self.height - 50)
            #
            d.vbox.pack_start(lbl_info, expand=False, padding=10)
            d.vbox.pack_start(scrollw, expand=True, padding=10)
            #
            d.vbox.show_all()
            #        
            ret = d.run()
            d.destroy()
            #
        

    def product_flow(self, widget):
        self.product_flow_dialog = gtk.Dialog('Flow Control', 
            self.parent, gtk.DIALOG_MODAL,
            (gtk.STOCK_CLOSE, gtk.RESPONSE_ACCEPT))
        self.product_flow_dialog.set_size_request(
            self.width - 100, self.height - 50)
        #
        combo_type = gtk.combo_box_new_text()
        combo_type.append_text('IN')
        combo_type.append_text('OUT')
        combo_type.set_active(0)
        #
        cal = gtk.Calendar()
        bgcolor = gtk.gdk.Color(250*255, 255*255, 210*255)
        #
        lstore = gtk.ListStore(str, str, str)
        trview = gtk.TreeView(lstore)
        trvcol_prd = gtk.TreeViewColumn('Product')
        trvcol_prd.set_min_width(300)
        cell_prd = gtk.CellRendererCombo()
        cell_prd.set_property('text-column', 0)
        cell_prd.set_property('editable', True)
        cell_prd.set_property('has-entry', False)
        cell_prd.set_property('model', self.product_flow_get_idames_model())
        cell_prd.set_property('cell-background-gdk', bgcolor)
        cell_prd.connect('edited', self.product_flow_combo_edited, trview, 0)
        trvcol_prd.pack_start(cell_prd, True)
        trvcol_prd.set_attributes(cell_prd, text=0)
        trvcol_amt = gtk.TreeViewColumn('Amount')
        trvcol_amt.set_min_width(120)
        cell_amt = gtk.CellRendererText()
        cell_amt.set_property('editable', True)
        cell_amt.set_property('cell-background-gdk', bgcolor)
        cell_amt.connect('edited', self.product_flow_cell_edited, lstore, 1)
        trvcol_amt.pack_start(cell_amt, True)
        trvcol_amt.set_attributes(cell_amt, text=1)
        trvcol_note = gtk.TreeViewColumn('Note')
        trvcol_note.set_min_width(120)
        cell_note = gtk.CellRendererText()
        cell_note.set_property('editable', True)
        cell_note.set_property('cell-background-gdk', bgcolor)
        cell_note.connect('edited', self.product_flow_cell_edited, lstore, 2)
        trvcol_note.pack_start(cell_note, True)
        trvcol_note.set_attributes(cell_note, text=2)
        trview.append_column(trvcol_prd)
        trview.append_column(trvcol_amt)
        trview.append_column(trvcol_note)
        #
        scrollw = gtk.ScrolledWindow()
        scrollw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollw.add(trview)
        #
        btn_new = gtk.Button(stock=gtk.STOCK_NEW)
        btn_new.connect('clicked', self.product_flow_new_entry, trview)
        btn_delete = gtk.Button(stock=gtk.STOCK_DELETE)
        btn_delete.connect('clicked', self.product_flow_delete_entry, trview)
        btn_save = gtk.Button(stock=gtk.STOCK_SAVE)
        btn_save.connect('clicked', self.product_flow_save, combo_type, cal, trview, cell_prd)
        btnbox = gtk.HButtonBox()
        btnbox.set_spacing(10)
        btnbox.set_layout(gtk.BUTTONBOX_END)
        btnbox.pack_start(btn_new)
        btnbox.pack_start(btn_delete)
        btnbox.pack_start(btn_save)
        #
        self.product_flow_dialog.vbox.pack_start(combo_type, expand=False,
            padding=4)
        self.product_flow_dialog.vbox.pack_start(cal, expand=False,
            padding=4)            
        self.product_flow_dialog.vbox.pack_start(scrollw, expand=True,
            padding=4)            
        self.product_flow_dialog.vbox.pack_start(btnbox, expand=False,
            padding=4)            
        self.product_flow_dialog.vbox.show_all()
        #        
        ret = self.product_flow_dialog.run()
        self.product_flow_dialog.destroy()
        #
        return ret        
        
        
    def product_new(self, widget):
        d = gtk.Dialog('New Product', self.parent, gtk.DIALOG_MODAL,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        d.set_size_request(self.app.main_win_width - 100, -1)

        tbl_prd = gtk.Table(6, 3)        
        #
        ent_id = gtk.Entry()
        lbl_id = gtk.Label('Product ID')
        lbl_id.set_alignment(0, 0.5)
        tbl_prd.attach(lbl_id, 0, 1, 0, 1, xpadding=8, ypadding=8)
        tbl_prd.attach(ent_id, 1, 3, 0, 1, xpadding=8, ypadding=8)
        #
        ent_pname = gtk.Entry()
        lbl_pname = gtk.Label('Product Name')
        lbl_pname.set_alignment(0, 0.5)
        tbl_prd.attach(lbl_pname, 0, 1, 1, 2, xpadding=8, ypadding=8)
        tbl_prd.attach(ent_pname, 1, 3, 1, 2, xpadding=8, ypadding=8)
        #
        ent_price = gtk.Entry()
        lbl_price = gtk.Label('Price')
        lbl_price.set_alignment(0, 0.5)
        tbl_prd.attach(lbl_price, 0, 1, 2, 3, xpadding=8, ypadding=8)
        tbl_prd.attach(ent_price, 1, 3, 2, 3, xpadding=8, ypadding=8)
        #
        combo_unit = gtk.combo_box_new_text()
        self.product_populate_units(combo=combo_unit)
        lbl_unit = gtk.Label('Unit')
        lbl_unit.set_alignment(0, 0.5)
        tbl_prd.attach(lbl_unit, 0, 1, 3, 4, xpadding=8, ypadding=8)
        tbl_prd.attach(combo_unit, 1, 3, 3, 4, xpadding=8, ypadding=8)
        #
        combo_cat = gtk.combo_box_new_text()
        self.product_populate_categories(combo=combo_cat)
        lbl_cat = gtk.Label('Category')
        lbl_cat.set_alignment(0, 0.5)
        tbl_prd.attach(lbl_cat, 0, 1, 4, 5, xpadding=8, ypadding=8)
        tbl_prd.attach(combo_cat, 1, 3, 4, 5, xpadding=8, ypadding=8)
        #
        ent_minstock = gtk.Entry()
        lbl_minstock = gtk.Label('Min Stock')
        lbl_minstock.set_alignment(0, 0.5)
        tbl_prd.attach(lbl_minstock, 0, 1, 5, 6, xpadding=8, ypadding=8)
        tbl_prd.attach(ent_minstock, 1, 3, 5, 6, xpadding=8, ypadding=8)
        #

        d.vbox.pack_start(tbl_prd)
        d.vbox.show_all()
        #
        ret = d.run()
        d.hide()
        
        if ret == gtk.RESPONSE_ACCEPT:
            pid = ent_id.get_text().strip()
            pname = ent_pname.get_text().strip()
            price = ent_price.get_text().strip()
            try:
                price2 = float(price)
            except:
                price2 = 0
            unit = combo_unit.get_active_text()
            uid = 0
            if unit:
                uid = self.get_unit_id(unit)
            cat = combo_cat.get_active_text()
            cid = 0
            if cat:
                cid = self.get_category_id(cat)
            minstock = ent_minstock.get_text().strip()
            try:
                minstock2 = int(minstock)
            except:
                minstock2 = 0

            
            if not id or not pname:
                msg = 'ID and Product Name could not be left blank'
                gtkutils.error(parent=self.parent, message=msg, 
                    title='Error')
            else:
                found = self.get_product(pid)
                if found:
                    msg = 'Product %s already exists' %(pid)
                    gtkutils.error(message=msg, parent=d, title='Error')
                else:
                    q = '''
                    insert into ms_products(id, product_name, price, uid, cid, stock,minstock)
                    values(?,?,?,?,?,?,?)    
                    '''
                    a = (pid, pname, price2, uid, cid, 0, minstock2)
                    r = self.db.query(q, a, self.app.database)
                    if r[0] != 0:
                        msg = r[1]
                        dialog = gtkutils.error
                        dialog(title='Error', message=msg, parent=d)
                    #
                    self.draw_products()
        #
        d.destroy()

    def product_edit(self, widget):
        selection = self.trview_main.get_selection()
        model, selected = selection.get_selected_rows()
        iters = [model.get_iter(path) for path in selected]
        if iters:
            iter = iters[0]
            id = model.get_value(iter, 0)
            product = self.get_product(id)
            #
            d = gtk.Dialog('Edit Product', self.parent, gtk.DIALOG_MODAL,
                (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                    gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
            d.set_size_request(self.app.main_win_width - 100, -1)

            tbl_prd = gtk.Table(5, 3)        
            #
            lbl_id2 = gtk.Label(id)
            lbl_id2.set_alignment(0, 0.5)
            lbl_id = gtk.Label('Product ID')
            lbl_id.set_alignment(0, 0.5)
            tbl_prd.attach(lbl_id, 0, 1, 0, 1, xpadding=8, ypadding=8)
            tbl_prd.attach(lbl_id2, 1, 3, 0, 1, xpadding=8, ypadding=8)
            #
            ent_pname = gtk.Entry()
            ent_pname.set_text(product[1])
            lbl_pname = gtk.Label('Product Name')
            lbl_pname.set_alignment(0, 0.5)
            tbl_prd.attach(lbl_pname, 0, 1, 1, 2, xpadding=8, ypadding=8)
            tbl_prd.attach(ent_pname, 1, 3, 1, 2, xpadding=8, ypadding=8)
            #
            ent_price = gtk.Entry()
            ent_price.set_text(str(product[2]))
            lbl_price = gtk.Label('Price')
            lbl_price.set_alignment(0, 0.5)
            tbl_prd.attach(lbl_price, 0, 1, 2, 3, xpadding=8, ypadding=8)
            tbl_prd.attach(ent_price, 1, 3, 2, 3, xpadding=8, ypadding=8)
            #
            combo_unit = gtk.combo_box_new_text()
            uid = product[3]
            unit = self.get_unit_name(uid)
            self.product_populate_units(combo=combo_unit, active=unit)
            lbl_unit = gtk.Label('Unit')
            lbl_unit.set_alignment(0, 0.5)
            tbl_prd.attach(lbl_unit, 0, 1, 3, 4, xpadding=8, ypadding=8)
            tbl_prd.attach(combo_unit, 1, 3, 3, 4, xpadding=8, ypadding=8)
            #
            combo_cat = gtk.combo_box_new_text()
            cid = product[4]
            cat = self.get_category_name(cid)
            self.product_populate_categories(combo=combo_cat, active=cat)
            lbl_cat = gtk.Label('Category')
            lbl_cat.set_alignment(0, 0.5)
            tbl_prd.attach(lbl_cat, 0, 1, 4, 5, xpadding=8, ypadding=8)
            tbl_prd.attach(combo_cat, 1, 3, 4, 5, xpadding=8, ypadding=8)
            #
            ent_minstock = gtk.Entry()
            ent_minstock.set_text(str(product[6]))
            lbl_minstock = gtk.Label('Min Stock')
            lbl_minstock.set_alignment(0, 0.5)
            tbl_prd.attach(lbl_minstock, 0, 1, 5, 6, xpadding=8, ypadding=8)
            tbl_prd.attach(ent_minstock, 1, 3, 5, 6, xpadding=8, ypadding=8)

            #
            d.vbox.pack_start(tbl_prd)
            d.vbox.show_all()
            #
            ret = d.run()
            d.hide()
            
            if ret == gtk.RESPONSE_ACCEPT:
                pname = ent_pname.get_text().strip()
                price = ent_price.get_text().strip()
                try:
                    price2 = float(price)
                except:
                    price2 = 0
                unit = combo_unit.get_active_text()
                uid = 0
                if unit:
                    uid = self.get_unit_id(unit)
                cat = combo_cat.get_active_text()
                cid = 0
                if cat:
                    cid = self.get_category_id(cat)
                minstock = ent_minstock.get_text().strip()
                try:
                    minstock2 = int(minstock)
                except:
                    minstock2 = 0
                
                if not pname:
                    msg = 'Product Name could not be left blank'
                    gtkutils.error(parent=self.parent, message=msg, 
                        title='Error')
                else:
                    q = '''
                    update ms_products set product_name=?, price=?, uid=?, cid=?, minstock=? 
                    where id=?    
                    '''
                    a = (pname, price2, uid, cid, minstock2, id)
                    r = self.db.query(q, a, self.app.database)
                    if r[0] != 0:
                        msg = r[1]
                        dialog = gtkutils.error
                        dialog(title='Error', message=msg, parent=d)
                    #
                    self.draw_products()
            #
            d.destroy()
                

    def product_delete(self, widget):
        selection = self.trview_main.get_selection()
        model, selected = selection.get_selected_rows()
        iters = [model.get_iter(path) for path in selected]
        if iters:
            ids = [model.get_value(iter, 0) for iter in iters]
            names = [model.get_value(iter, 1) for iter in iters]
            
            count = len(ids)
            info_delete_str = '\n'.join(names)
            #
            if count > 0:
                msg = 'Are you sure you want to '
                msg += 'delete %d product(s)?' %(count)
                msg2 = 'Selected product(s):\n' + info_delete_str
                msg2 += '\n\nAll corresponding data will also be deleted.'
                msg2 += '\nThis action can not be undone.'
                
                ok = gtkutils.confirm(title='Please confirm', 
                    message=msg, message2=msg2, parent=self.parent,
                    buttons=gtk.BUTTONS_YES_NO)

                #if yes,
                if ok == gtk.RESPONSE_YES:
                    q = []
                    for id in ids:
                        query = 'delete from ms_products where id=?'
                        args = (id,)
                        temp = (query, args)
                        q.append(temp)
                    r = self.db.query_transact(q, self.app.database)
                    if r[0] != 0:
                        msg = r[1]
                        dialog = gtkutils.error
                        dialog(title='Error', message=msg, parent=self.parent)
                    #
                    self.draw_products()


    def product_refresh(self, widget):
        self.draw_products()
    
    def product_populate_categories(self, combo, active=''):
        categories = self.get_categories()
        category_name = [x[1] for x in categories]
        #
        model = combo.get_model()
        model.clear()
        #
        combo.append_text('')
        i = 1
        activeindex = 0
        for c in category_name:
            combo.append_text(c)
            if c == active:
                activeindex = i
            i += 1
        if active:
            combo.set_active(activeindex)
        else:
            combo.set_active(0)

    def product_populate_units(self, combo, active=''):
        units = self.get_units()
        units_name = [x[1] for x in units]
        #
        model = combo.get_model()
        model.clear()
        #
        combo.append_text('')
        i = 1
        activeindex = 0
        for u in units_name:
            combo.append_text(u)
            if u == active:
                activeindex = i
            i += 1
        if active:
            combo.set_active(activeindex)
        else:
            combo.set_active(0)

    def category_rename(self, widget):
        category = self.combo_cat.get_active_text()
        if category:
            newcat = gtkutils.input(title='Rename Category', label='New category name',
            parent=self.cat_edit_dialog, default=category).strip().upper()
            if newcat and newcat != category:
                categories = self.get_categories()
                found=self.get_category_id(newcat)
                if found:
                    msg = 'Category %s already exists' %(newcat)
                    gtkutils.error(title='Error', message=msg, 
                        parent=self.parent)
                else:
                    q = '''
                    update ms_categories set category_name=? where category_name=?
                    '''
                    a = (newcat, category)
                    r = self.db.query(q, a, self.app.database)
                    if r[0] != 0:
                        msg = r[1]
                        dialog = gtkutils.error
                        dialog(title='Error', message=msg, parent=self.cat_edit_dialog)
                    else:
                        self.product_populate_categories(combo=self.combo_cat, active=newcat)
                    

    def category_new(self, widget):
        category = gtkutils.input(title='New Category', label='Category name',
            parent=self.cat_edit_dialog).strip().upper()
        if category:
            categories = self.get_categories()
            found=self.get_category_id(category)
            #
            if found:
                msg = 'Category %s already exists' %(category)
                gtkutils.error(title='Error', message=msg, 
                    parent=self.parent)
            else:
                q = '''
                insert into ms_categories(category_name, note)
                values(?,?)
                '''
                a = (category,'')
                r = self.db.query(q, a, self.app.database)
                if r[0] != 0:
                    msg = r[1]
                    dialog = gtkutils.error
                    dialog(title='Error', message=msg, parent=self.cat_edit_dialog)
                else:
                    self.product_populate_categories(active=category, combo=self.combo_cat)
                
    
    def category_delete(self, widget):
        category = self.combo_cat.get_active_text()
        if category:
            cid = self.get_category_id(category)
            members = self.get_category_members(cid)
            members_count = len(members)
            if members_count:
                msg = '''Category has %d member(s).\nAre you sure you want to delete category %s?\nAll products in this category will lose it's category information.''' %(
                members_count, category)
            else:
                msg = '''Are you sure you want to delete category %s?''' %(category)
            #
            ok = gtkutils.confirm(title='Please confirm', message=msg, 
                parent=self.cat_edit_dialog, buttons=gtk.BUTTONS_YES_NO)
            if ok == gtk.RESPONSE_YES:
                q1 = '''
                update ms_products set cid=0 where cid=?
                '''
                a1 = (cid,)
                q2 = '''
                delete from ms_categories where id=?
                '''
                a2 = (cid,)
                q = ((q1, a1), (q2, a2))
                r = self.db.query_transact(q, self.app.database)
                if r[0] == 0:
                    msg = 'Category %s has been deleted successfully' %(category)
                    dialog = gtkutils.info
                else:
                    msg = r[1]
                    dialog = gtkutils.error
                dialog(title='Result', message=msg, parent=self.cat_edit_dialog)
                #
                self.product_populate_categories(combo=self.combo_cat)
                self.combo_cat.popup()
                
    
    def category_save(self, widget):
        category = self.combo_cat.get_active_text()
        if category:
            cid = self.get_category_id(category)
            model = self.cat_propedit.model
            iter = model.get_iter_first()
            note = model.get_value(iter, 1)
            #
            q = '''
            update ms_categories set note=? where id=?
            '''
            a = (note, cid)
            r = self.db.query(q, a, self.app.database)
            if r[0] == 0:
                msg = 'Settings for category %s has been saved successfully' %(category)
                dialog = gtkutils.info
            else:
                msg = r[1]
                dialog = gtkutils.error
            dialog(title='Result', message=msg, parent=self.cat_edit_dialog)
            #
                
            
    def category_get_prop(self, combo):
        category = combo.get_active_text()
        if category:
            self.cat_propedit.clear()
            note = self.get_category_note(category)
            cid = self.get_category_id(category)
            data = (('Note', note),)
            self.cat_propedit.fill(data)
            members = self.get_category_members(cid)
            members_info = 'Member count: %d' %(len(members))
        else:
            self.cat_propedit.clear()
            members_info = ''
        self.lbl_cat_members.set_text(members_info)
        
    
    def category_edit(self, widget):
        self.cat_edit_dialog = gtk.Dialog('Category Editor', 
            self.parent, gtk.DIALOG_MODAL,
            (gtk.STOCK_CLOSE, gtk.RESPONSE_ACCEPT))
        self.cat_edit_dialog.set_size_request(
            self.width - 100, self.height - 100)
        #        
        hbox = gtk.HBox()
        vbox = gtk.VBox()
        #
        self.combo_cat = gtk.combo_box_new_text()
        self.product_populate_categories(combo=self.combo_cat)
        #
        self.cat_propedit = gtkutils.SimplePropertyEditor()
        #
        vbox.pack_start(self.combo_cat, padding=4, expand=False)
        vbox.pack_start(self.cat_propedit.scrolledwin, padding=4)
        #
        btnbox = gtk.VButtonBox()
        btnbox.set_spacing(10)
        btnbox.set_layout(gtk.BUTTONBOX_START)
        btn_save = gtk.Button(stock=gtk.STOCK_SAVE)
        btn_save.get_children()[0].get_children()[0].get_children()[1].set_text('Save settings')
        btn_save.connect('clicked', self.category_save)
        btn_del = gtk.Button(stock=gtk.STOCK_DELETE)
        btn_del.connect('clicked', self.category_delete)
        btn_rename = gtk.Button(stock=gtk.STOCK_EDIT)
        btn_rename.get_children()[0].get_children()[0].get_children()[1].set_text('Rename')
        btn_rename.connect('clicked', self.category_rename)
        btn_new = gtk.Button(stock=gtk.STOCK_NEW)
        btn_new.connect('clicked', self.category_new)
        btnbox.pack_start(btn_save)
        btnbox.pack_start(btn_rename)
        btnbox.pack_start(btn_del)
        btnbox.pack_start(btn_new)
        #
        self.lbl_cat_members = gtk.Label()
        self.lbl_cat_members.set_alignment(0.02, 0.5)
        #
        hbox.pack_start(vbox, padding=8)
        hbox.pack_start(btnbox, expand=False, padding=8)
        #
        self.combo_cat.connect('changed', self.category_get_prop)
        #        
        self.cat_edit_dialog.vbox.pack_start(hbox, padding=4)
        self.cat_edit_dialog.vbox.pack_start(self.lbl_cat_members, padding=4,
            expand=False)
        self.cat_edit_dialog.vbox.show_all()
        #        
        ret = self.cat_edit_dialog.run()
        self.cat_edit_dialog.destroy()
        #
        self.draw_products()
        return ret        


    def unit_rename(self, widget):
        unit = self.combo_unit.get_active_text()
        if unit:
            newunit = gtkutils.input(title='Rename Unit', label='New unit name',
            parent=self.unit_edit_dialog, default=unit).strip().upper()
            if newunit and newunit != unit:
                found=self.get_unit_id(newunit)
                if found:
                    msg = 'Unit %s already exists' %(newunit)
                    gtkutils.error(title='Error', message=msg, 
                        parent=self.parent)
                else:
                    q = '''
                    update ms_units set unit_name=? where unit_name=?
                    '''
                    a = (newunit, unit)
                    r = self.db.query(q, a, self.app.database)
                    if r[0] != 0:
                        msg = r[1]
                        dialog = gtkutils.error
                        dialog(title='Error', message=msg, parent=self.unit_edit_dialog)
                    else:
                        self.product_populate_units(combo=self.combo_unit, active=newunit)
                    

    def unit_new(self, widget):
        unit = gtkutils.input(title='New Unit', label='Unit name',
            parent=self.unit_edit_dialog).strip().upper()
        if unit:
            found=self.get_unit_id(unit)
            #
            if found:
                msg = 'Unit %s already exists' %(unit)
                gtkutils.error(title='Error', message=msg, 
                    parent=self.parent)
            else:
                q = '''
                insert into ms_units(unit_name, note)
                values(?,?)
                '''
                a = (unit,'')
                r = self.db.query(q, a, self.app.database)
                if r[0] != 0:
                    msg = r[1]
                    dialog = gtkutils.error
                    dialog(title='Error', message=msg, parent=self.unit_edit_dialog)
                else:
                    self.product_populate_units(active=unit, combo=self.combo_unit)
    
    def unit_delete(self, widget):
        unit = self.combo_unit.get_active_text()
        if unit:
            uid = self.get_unit_id(unit)
            members = self.get_unit_members(uid)
            members_count = len(members)
            if members_count:
                msg = '''Unit has %d member(s).\nAre you sure you want to delete unit %s?\nAll products in this unit will lose it's unit information.''' %(
                members_count, unit)
            else:
                msg = '''Are you sure you want to delete unit %s?''' %(unit)
            #
            ok = gtkutils.confirm(title='Please confirm', message=msg, 
                parent=self.unit_edit_dialog, buttons=gtk.BUTTONS_YES_NO)
            if ok == gtk.RESPONSE_YES:
                q1 = '''
                update ms_products set uid=0 where uid=?
                '''
                a1 = (uid,)
                q2 = '''
                delete from ms_units where id=?
                '''
                a2 = (uid,)
                q = ((q1, a1), (q2, a2))
                r = self.db.query_transact(q, self.app.database)
                if r[0] == 0:
                    msg = 'Unit %s has been deleted successfully' %(unit)
                    dialog = gtkutils.info
                else:
                    msg = r[1]
                    dialog = gtkutils.error
                dialog(title='Result', message=msg, parent=self.unit_edit_dialog)
                #
                self.product_populate_units(combo=self.combo_unit)
                self.combo_unit.popup()
    
    def unit_save(self, widget):
        unit = self.combo_unit.get_active_text()
        if unit:
            uid = self.get_unit_id(unit)
            model = self.unit_propedit.model
            iter = model.get_iter_first()
            note = model.get_value(iter, 1)
            #
            q = '''
            update ms_units set note=? where id=?
            '''
            a = (note, uid)
            r = self.db.query(q, a, self.app.database)
            if r[0] == 0:
                msg = 'Settings for unit %s has been saved successfully' %(unit)
                dialog = gtkutils.info
            else:
                msg = r[1]
                dialog = gtkutils.error
            dialog(title='Result', message=msg, parent=self.unit_edit_dialog)
            #
                
    def unit_get_prop(self, combo):
        unit = combo.get_active_text()
        if unit:
            self.unit_propedit.clear()
            note = self.get_unit_note(unit)
            uid = self.get_unit_id(unit)
            data = (('Note', note),)
            self.unit_propedit.fill(data)
            members = self.get_unit_members(uid)
            members_info = 'Member count: %d' %(len(members))
        else:
            self.unit_propedit.clear()
            members_info = ''
        self.lbl_unit_members.set_text(members_info)
        
    
    def unit_edit(self, widget):
        self.unit_edit_dialog = gtk.Dialog('Unit Editor', 
            self.parent, gtk.DIALOG_MODAL,
            (gtk.STOCK_CLOSE, gtk.RESPONSE_ACCEPT))
        self.unit_edit_dialog.set_size_request(
            self.width - 100, self.height - 100)
        #        
        hbox = gtk.HBox()
        vbox = gtk.VBox()
        #
        self.combo_unit = gtk.combo_box_new_text()
        self.product_populate_units(combo=self.combo_unit)
        #
        self.unit_propedit = gtkutils.SimplePropertyEditor()
        #
        vbox.pack_start(self.combo_unit, padding=4, expand=False)
        vbox.pack_start(self.unit_propedit.scrolledwin, padding=4)
        #
        btnbox = gtk.VButtonBox()
        btnbox.set_spacing(10)
        btnbox.set_layout(gtk.BUTTONBOX_START)
        btn_save = gtk.Button(stock=gtk.STOCK_SAVE)
        btn_save.get_children()[0].get_children()[0].get_children()[1].set_text('Save settings')
        btn_save.connect('clicked', self.unit_save)
        btn_del = gtk.Button(stock=gtk.STOCK_DELETE)
        btn_del.connect('clicked', self.unit_delete)
        btn_rename = gtk.Button(stock=gtk.STOCK_EDIT)
        btn_rename.get_children()[0].get_children()[0].get_children()[1].set_text('Rename')
        btn_rename.connect('clicked', self.unit_rename)
        btn_new = gtk.Button(stock=gtk.STOCK_NEW)
        btn_new.connect('clicked', self.unit_new)
        btnbox.pack_start(btn_save)
        btnbox.pack_start(btn_rename)
        btnbox.pack_start(btn_del)
        btnbox.pack_start(btn_new)
        #
        self.lbl_unit_members = gtk.Label()
        self.lbl_unit_members.set_alignment(0.02, 0.5)
        #
        hbox.pack_start(vbox, padding=8)
        hbox.pack_start(btnbox, expand=False, padding=8)
        #
        self.combo_unit.connect('changed', self.unit_get_prop)
        #        
        self.unit_edit_dialog.vbox.pack_start(hbox, padding=4)
        self.unit_edit_dialog.vbox.pack_start(self.lbl_unit_members, padding=4,
            expand=False)
        self.unit_edit_dialog.vbox.show_all()
        #        
        ret = self.unit_edit_dialog.run()
        self.unit_edit_dialog.destroy()
        #
        self.draw_products()
        return ret        
