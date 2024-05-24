import psycopg2
import psycopg2.extras
import os

if 'POSTGRES_PASSWORD_FILE' in os.environ:
    with open(os.environ['POSTGRES_PASSWORD_FILE'], 'r') as f:
        password = f.read().strip()
else:
    password = os.environ['POSTGRES_PASSWORD']

def db_connect():
    global conn
    """ DOCKER """
    # conn = psycopg2.connect(host="db", user="postgres", password=password, database="test_axe")
    """ RENDER """
    conn = psycopg2.connect('DB_URL')

    global CUR
    CUR = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    return CUR, conn