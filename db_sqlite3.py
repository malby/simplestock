#
# (c) Noprianto, 2008-2009, GPL
#

sqlite3 = None

try:
    import sqlite3
except ImportError:
    try:
        from pysqlite2 import dbapi2 as sqlite3
    except ImportError:
        pass

if sqlite3:
    db = sqlite3
else:
    db = None
    raise ImportError, 'Could not find any sqlite3 module.'

#
def query(query, args, dbfile, engine=db):
    if not engine:
        return [1, 'Engine not specified.',None]
    #
    ret_data = []
    ret = []
    try:
        conn = engine.connect(dbfile)
        cur = conn.cursor()
        cur.execute(query, args)
        ret_data = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        ret = [0, ret_data, cur.lastrowid]
    except Exception, e:
        ret = [2, e.message, None] 
    #
    return ret

def query_transact(query_args, dbfile, engine=db):
    if not engine:
        return [1, 'Engine not specified.',None]
    #
    ret_data = []
    ret = []
    try:
        conn = engine.connect(dbfile)
        cur = conn.cursor()
        for q in query_args:
            query = q[0]
            args = q[1]
            cur.execute(query, args)
            ret_data = cur.fetchall()
            ret = [0, ret_data, cur.lastrowid]
    except Exception, e:
        conn.rollback()
        ret = [2, e.message, None] 
    else:
        conn.commit()
    finally:
        cur.close()
        conn.close()

    #
    return ret
