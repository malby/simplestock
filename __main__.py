#!/usr/bin/env python

#
#application main program
#
#
#
#(c) Noprianto <nop@tedut.com>, 2008-2009, GPL

def _check_db():
    ret = (1, 'Could not load database module.')
    try:
        import db_sqlite3
        ret = (0, '')
    except ImportError:
        pass

    return ret


def _check_main():
    ret = (2, 'Could not load UI main module.')
    try:
        import ui_main
        ret = (0, '')
    except:
        pass
    else:
        del ui_main
    return ret

def _check_gtk():
    ret = (3, 'Could not load GTK+ module.')
    try:
        import gtk
        ret = (0, '')
    except ImportError:
        pass
    else:
        del gtk
    return ret

def _check_pygtk2():
    ret = (4, 'Could not load PyGTK+ module.')
    try:
        import pygtk
        pygtk.require('2.0')
        ret = (0, '')
    except ImportError:
        pass
    else:
        del pygtk
    return ret

def dependency_check():
    error_val = 0
    error_msg = []
    #
    result_check_db = _check_db()
    if result_check_db[0] != 0:
        error_val += result_check_db[0]
        error_msg.append(result_check_db[1])
    #    
    result_check_main = _check_main()
    if result_check_main[0] != 0:
        error_val += result_check_main[0]
        error_msg.append(result_check_main[1])
    #
    result_check_gtk = _check_gtk()
    if result_check_gtk[0] != 0:
        error_val += result_check_gtk[0]
        error_msg.append(result_check_gtk[1])
    #
    result_check_pygtk2 = _check_pygtk2()
    if result_check_pygtk2[0] != 0:
        error_val += result_check_pygtk2[0]
        error_msg.append(result_check_pygtk2[1])

    if error_val:
        ret = (False, error_msg)
    else:
        ret = (True, error_msg)
    return ret

if __name__ == '__main__':
    dep = dependency_check()
    if dep[0]:
        #
        import gtk
        import pygtk
        #
        from ui_main import UIMain
        #
        ui_main = UIMain()
        gtk.main()
    else:
        #put real error message here, 
        #only minimal module used here!!
        print dep

