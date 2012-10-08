#
# 
# (c) Noprianto, 2008-2009, GPL
#

import md5
import os

#application class
class Application:
    def __init__(self):
        #basic properties
        self.name = 'SimpleStock'
        self.version = (0, 9, 5)
        self.version_str = '.'.join([str(x) for x in self.version])
        self.company = 'tedut.com'
        self.website = 'http://www.tedut.com'
        self.authors = ('Noprianto <nop@tedut.com>')
        self.year = (2008, 2009)
        self.year_str = ','.join([str(x) for x in self.year])
        self.copyright_str = '(c) %s, %s' %(self.year_str, self.company)
        self.main_title = '%s %s' %(self.name, self.version_str)
        #
        #date time format
        self.date_time_format = '%a, %d %b %Y - %H:%M:%S'
        self.time_format = '%H:%M:%S'
        self.date_format = '%a, %d %b %Y' 
        #
        #directories, database, logo
        self.datadir = './data/'
        self.imgdir = self.datadir + 'img/'
        self.logofile = './logo.png'
        self.database = self.datadir +  'data.db'
        #
        #screen related
        screen_width = 780 #or?# int(gtk.gdk.screen_width() * 0.9)
        screen_height = 580 #or?# int(gtk.gdk.screen_height() * 0.8)
        if screen_width <= 640:
            self.main_win_width = 620
        else:
            self.main_win_width = screen_width 
        #
        if screen_height <= 480:
            self.main_win_height = 420
        else:
            self.main_win_height = screen_height 
        #
        #tabs, user interface, resources        
        #
        self.tabs = ( ('User', 'user.png'),
                      ('Product', 'product.png'),
                      ('Change Password', 'passwd.png'),
                      ('About', 'about.png'),
                    ) 
        self.resource_all = [x[0].upper() for x in self.tabs]
        self.resource_all_str = ','.join(self.resource_all)
        #
        

    def init_db_query(self):
        ret = []
        #groups
        query = '''
        CREATE TABLE ms_groups(id integer primary key autoincrement,
        group_name text, resources text)
        '''
        ret.append(query)
        #        
        query = '''
        INSERT INTO ms_groups(group_name, resources) 
            VALUES('ADMIN', '%s')
        ''' %(self.resource_all_str)
        ret.append(query)
        #
        
        #users
        query = '''
        CREATE TABLE ms_users(id integer primary key autoincrement,
        user_name text, real_name text, gid integer references 
        ms_groups(id), password text)
        '''
        ret.append(query)
        #        
        passwd = 'admin'
        passwd_md5 = md5.new(passwd).hexdigest() 
        query = '''
        INSERT INTO ms_users(user_name, real_name, gid, password) 
            VALUES('admin', 'Administrator', 1, '%s')
        ''' %(passwd_md5)
        ret.append(query)
        #

        #categories
        query = '''
        CREATE TABLE ms_categories(id integer primary key autoincrement,
        category_name text, note text)
        '''
        ret.append(query)
        #        

        #units
        query = '''
        CREATE TABLE ms_units(id integer primary key autoincrement,
        unit_name text, note text)
        '''
        ret.append(query)
        #        

        #products
        query = '''
        CREATE TABLE ms_products(id text primary key, 
        product_name text, price real, uid integer references ms_units(id),
        cid integer references ms_categories(id), stock integer, minstock integer)
        '''
        ret.append(query)
        #        

        #products flow
        query = '''
        CREATE TABLE tr_flow(id integer primary key autoincrement, 
        dateinfo text, 
        user text,
        pid text references ms_products(id),
        flow_type text, amount integer, note text)
        '''
        ret.append(query)
        #        
        

        return ret
