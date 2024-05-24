import psycopg2
import psycopg2.extras
import os

if 'POSTGRES_PASSWORD_FILE' in os.environ:
    with open(os.environ['POSTGRES_PASSWORD_FILE'], 'r') as f:
        password = f.read().strip()
    host="db"
    username="postgres"
else:
    password = os.environ['POSTGRES_PASSWORD']
    hostname = "dpg-cp8bbe21hbls739vnffg-a"
    port = "5432"
    username = "test_axe_user"

def db_connect():
    global conn
    conn = psycopg2.connect(host=hostname, user=username, password=password, database="test_axe", port=port)

    global CUR
    CUR = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    return CUR, conn