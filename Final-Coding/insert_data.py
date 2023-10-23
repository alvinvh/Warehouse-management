import psycopg2
from config import config

def insert_data(table, data_list):

    sql = "INSERT INTO {}(barcode, name) VALUES(%s, %s)".format(table)
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql,data_list)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
        return "Successful!"
    except:
        return "Error!"
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    # insert multiple students
    '''insert_data('item',
        ('9300607180510', 'Item1', 1)

    )'''