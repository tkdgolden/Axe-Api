import psycopg2
from werkzeug.security import generate_password_hash

def db_connect():
    global conn
    conn = psycopg2.connect("dbname=test_axe")

    global CUR
    CUR = conn.cursor()

    return CUR

def add_judge(name, password):
    """ hash password, create new judge """

    pwhash = generate_password_hash(password)

    CUR.execute("""INSERT INTO judges(judge_name, pass_hash) VALUES (%(name)s, %(pwhash)s)""",
                {'name': name, 'pwhash': pwhash})

    conn.commit()