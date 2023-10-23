import psycopg2
from config import config


def update_contain(barcode_item, barcode_shelve, item_name, item_user):
    sql = """ UPDATE shelve
                SET contain_barcode = %s, contain_name = %s, item_user = %s
                WHERE barcode = %s"""
    conn = None
    updated_rows = 0
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute(sql, (barcode_item,item_name, item_user, barcode_shelve))
        # get the number of updated rows
        updated_rows = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        return "error"
    finally:
        if conn is not None:
            conn.close()

    return "Successful!"

def delete_db(table, barcode):
    """ update student name based on the student id """
    sql = """ DELETE FROM {}
                WHERE barcode = '{}'""".format(table, barcode)
    conn = None
    updated_rows = 0
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute(sql)
        # get the number of updated rows
        updated_rows = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if conn is not None:
            conn.close()

    return "Successful!"



