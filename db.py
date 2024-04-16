import psycopg2
import psycopg2.extras

def db_connect():
    global conn
    conn = psycopg2.connect("dbname=test_axe")

    global CUR
    CUR = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    return CUR, conn