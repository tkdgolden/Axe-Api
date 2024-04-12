import psycopg2

def db_connect():
    global conn
    conn = psycopg2.connect("dbname=axe-test-data user=tkdgolden")

    global CUR
    CUR = conn.cursor()