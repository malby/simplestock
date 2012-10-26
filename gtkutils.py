#
# (c) Noprianto <nop@tedut.com>, 2008-2009, GPL
#
#
try: 
   from hashlib import md5 as md5new
except ImportError:
   from md5 import new as md5new
#
import gtk
import pygtk
pygtk.require('2.0')

version = '9.1'

#-------------------------------DIALOGS--------------------------------#
def input(title='', label='Input', default='', password=False, 
    parent=None, flags=0):
    d = gtk.Dialog(title, parent, flags)
    d.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT)
    d.add_button(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT)
    #
    lbl_input = gtk.Label(label)
    ent_input = gtk.Entry()
    ent_input.set_text(default)
    ent_input.select_region(0, -1)
    if password:
        ent_input.set_visibility(False)
    #
    hb = gtk.HBox(False)
    hb.pack_start(lbl_input, padding=10, expand=False)
    hb.pack_start(ent_input, padding=10)
    #
    d.vbox.pack_start(hb, padding=20)
    d.vbox.show_all()
    #
    ret = ''
    dret = d.run()
    #
    if dret == gtk.RESPONSE_ACCEPT:
        ret = ent_input.get_text()
    #
    d.destroy()
    return ret

def __box(type, title, message, modal, parent, flags, buttons, 
    message2, image):
    #
    if modal:
        flags += gtk.DIALOG_MODAL
    #
    d = gtk.MessageDialog(parent=parent, flags=flags, type=type, 
        buttons=buttons)
    #
    d.set_markup(message)
    d.format_secondary_markup(message2)
    d.set_title(title)
    if image:
        image.show()
        d.set_image(image)
    dret = d.run()
    #
    d.destroy()
    ret = dret
    return ret
         
def info(title='', message='Information!', modal=True, 
    parent=None, flags=0, buttons=gtk.BUTTONS_OK, message2='', 
    image=None):
    ret = __box(type=gtk.MESSAGE_INFO,
        title=title, message=message, modal=modal,
        parent=parent, flags=flags, buttons=buttons, 
        message2=message2, image=image)
    return ret

def warning(title='', message='Warning!', modal=True, 
    parent=None, flags=0, buttons=gtk.BUTTONS_OK, message2='', 
    image=None):
    ret = __box(type=gtk.MESSAGE_WARNING,
        title=title, message=message, modal=modal,
        parent=parent, flags=flags, buttons=buttons, 
        message2=message2, image=image)
    return ret

def error(title='', message='Error!', modal=True, 
    parent=None, flags=0, buttons=gtk.BUTTONS_OK, message2='', 
    image=None):
    ret = __box(type=gtk.MESSAGE_ERROR,
        title=title, message=message, modal=modal,
        parent=parent, flags=flags, buttons=buttons, 
        message2=message2, image=image)
    return ret

def confirm(title='', message='Confirm?', modal=True, 
    parent=None, flags=0, buttons=gtk.BUTTONS_OK_CANCEL, message2='', 
    image=None):
    ret = __box(type=gtk.MESSAGE_QUESTION,
        title=title, message=message, modal=modal,
        parent=parent, flags=flags, buttons=buttons, 
        message2=message2, image=image)
    return ret
#----------------------------END-OF-DIALOGS----------------------------#

#----------------------------LOGIN DIALOGS-----------------------------#
def simple_login(validator, title='Login', username_label='User Name', 
    password_label='Password', parent=None, 
    error_message='Authentication Failed.', use_md5=True):
    tryagain = True
    while tryagain:
        uname = ''
        login_status = False
        #            
        d = gtk.Dialog(title, parent, gtk.DIALOG_MODAL,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
            gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))

        tbl = gtk.Table(2, 3)
        #
        ent_uname = gtk.Entry()
        lbl_uname = gtk.Label(username_label)
        lbl_uname.set_alignment(0, 0.5)
        tbl.attach(lbl_uname, 0, 1, 0, 1, xpadding=8, ypadding=8)
        tbl.attach(ent_uname, 1, 3, 0, 1, xpadding=8, ypadding=8)
        
        ent_passwd = gtk.Entry()
        ent_passwd.set_visibility(False)
        lbl_passwd = gtk.Label(password_label)
        lbl_passwd.set_alignment(0, 0.5)
        tbl.attach(lbl_passwd, 0, 1, 1, 2, xpadding=8, ypadding=8)
        tbl.attach(ent_passwd, 1, 3, 1, 2, xpadding=8, ypadding=8)
        
        vb = gtk.VBox()
        vb.pack_start(tbl, padding=10)
        
        d.vbox.pack_start(vb)
        d.vbox.show_all()
            
        ret = d.run()
            
        if ret == gtk.RESPONSE_ACCEPT:
            uname = ent_uname.get_text()
            passwd = ent_passwd.get_text()
            if use_md5:
                passwd2 = md5new(passwd).hexdigest()
            else:
                passwd2 = passwd
            
            if validator(uname, passwd2):
                login_status = True
                tryagain = False
            else:
                login_status = False
                tryagain = True
        else:
            login_status = False
            tryagain = False
        #
        d.destroy()
        if not login_status and tryagain:
            error(title='Error', message=error_message, parent=d)
        
    return (login_status, uname)
        
    
#----------------------------END-OF-LOGIN DIALOGS----------------------#


#-------------------------------HELP WINDOW----------------------------#
def tips(caption, tip, width=200, height=200, parent=None):
    w = gtk.Window(gtk.WINDOW_POPUP)
    w.set_transient_for(parent)
    w.set_position(gtk.WIN_POS_MOUSE)
    w.set_size_request(width, height)
    #
    caption2 =  '<b>%s</b>' %(caption)
    lbl_caption = gtk.Label()
    lbl_caption.set_markup(caption2)
    #
    textb = gtk.TextBuffer()
    textb.set_text(tip)
    textv = gtk.TextView(textb)
    textv.set_editable(False)
    #
    scrollw = gtk.ScrolledWindow()
    scrollw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    scrollw.add(textv)
    #
    btn_close = gtk.Button(stock=gtk.STOCK_CLOSE)
    btn_close.connect('clicked', lambda x: w.destroy())
    #
    vbox = gtk.VBox()
    vbox.pack_start(lbl_caption, expand=False, padding=8)
    vbox.pack_start(scrollw, expand=True, padding=8)
    vbox.pack_start(btn_close, expand=False, padding=8)
    hbox = gtk.HBox()
    hbox.pack_start(vbox, padding=8)
    #
    w.add(hbox)
    w.show_all()
#-----------------------------END-OF-HELP WINDOW-----------------------#

#-------------------------------PROPERTY EDITOR------------------------#
class SimplePropertyEditor:
    def __init__(self, property_label='Property', value_label='Value',
        property_width=120, value_width=160):
        self.property_label = property_label
        self.value_label = value_label
        self.property_width = property_width
        self.value_width = value_width
        #
        self.model = gtk.ListStore(str, str)
        self.treeview = gtk.TreeView(self.model)
        self.scrolledwin = gtk.ScrolledWindow()
        self.scrolledwin.set_policy(gtk.POLICY_AUTOMATIC, 
            gtk.POLICY_AUTOMATIC)
        self.scrolledwin.add(self.treeview)
        #        
        trvcol_prop = gtk.TreeViewColumn(self.property_label)
        trvcol_prop.set_min_width(self.property_width)
        trvcol_val = gtk.TreeViewColumn(self.value_label)
        trvcol_val.set_min_width(self.value_width)
        cell_prop = gtk.CellRendererText()
        cell_val = gtk.CellRendererText()
        cell_val.set_property('editable', True)
        cell_val.connect('edited', self.__edited)
        trvcol_prop.pack_start(cell_prop, True)
        trvcol_prop.set_attributes(cell_prop, text=0)
        self.treeview.append_column(trvcol_prop)
        trvcol_val.pack_start(cell_val, True)
        trvcol_val.set_attributes(cell_val, text=1)
        self.treeview.append_column(trvcol_val)
        #
        self.clear()
        #
    
    def __edited(self, cell, path, new_text):
        iter = self.model.get_iter(path)
        self.model.set_value(iter, 1, new_text)
    
    def clear(self):
        self.model.clear()
    
    def fill(self, data):
        self.clear()
        if data:
            for p in data:
                self.model.append(p)
        
#--------------------------END-OF-PROPERTY EDITOR----------------------#
