import psycopg2
from config import config

def get_table(table):
    """ query parts from the parts table """
    conn = None
    try:
        if table == None:
            pass
        else:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute("SELECT barcode, name FROM {} ORDER BY barcode".format(table))
            rows = cur.fetchall()
            #print("The number of parts: ", cur.rowcount)
            #for row in rows:
            #    print(row)
            cur.close()
            return rows

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def get_table_all(table):
    """ query parts from the parts table """
    conn = None
    try:
        if table == None:
            pass
        else:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute("SELECT * FROM {} ORDER BY barcode".format(table))
            rows = cur.fetchall()
            #print("The number of parts: ", cur.rowcount)
            #for row in rows:
            #    print(row)
            cur.close()
            return rows

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def get_dropdownlist_name(table):
    list = get_table(table)
    list_2 = []
    for i in list:
        list_2.append(i[1])
    return list_2

def get_dropdownlist_barcode(table):
    list = get_table(table)
    list_2 = []
    for i in list:
        list_2.append(i[0])
    return list_2

def get_barcode(table, name):
    """ query parts from the parts table """
    conn = None
    try:
        if table == None:
            pass
        else:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute("SELECT * FROM {} WHERE NAME = '{}'".format(table, name))
            rows = cur.fetchall()
            #print("The number of parts: ", cur.rowcount)
            #for row in rows:
            #    print(row)
            cur.close()
            return rows[0][0]

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def get_name(table, barcode):
    """ query parts from the parts table """
    conn = None
    try:
        if table == None:
            pass
        else:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute("SELECT * FROM {} WHERE barcode = '{}'".format(table, barcode))
            rows = cur.fetchall()
            #print("The number of parts: ", cur.rowcount)
            #for row in rows:
            #    print(row)
            cur.close()
            return rows[0][1]

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def check_contain(barcode):
    conn = None
    try:
        if barcode == None:
            pass
        else:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute("""SELECT * FROM shelve WHERE barcode = '{}'""".format(barcode))
            rows = cur.fetchall()
            # print("The number of parts: ", cur.rowcount)
            # for row in rows:
            #    print(row)
            cur.close()
            print(rows)
            if rows[0][3] == '' or rows[0][3] == None:
                return "empty"
            else:
                return "fill"

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def get_login(username):
    conn = None
    try:
        if username == None:
            pass
        else:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute("SELECT pwd FROM userlogin WHERE username = '{}'".format(username))
            rows = cur.fetchone()
            # print("The number of parts: ", cur.rowcount)
            # for row in rows:
            #    print(row)
            cur.close()
            return str(rows).rstrip("',)").lstrip("('").rstrip(" ")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

#get_dropdownlist_barcode("shelve")
#print(get_dropdownlist_name("shelve"))
#print(get_barcode("shelve", "shelve1"))
#print(get_table("shelve"))
#print(check_contain('123123123'))