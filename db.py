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

    try:
        pwhash = generate_password_hash(password)

        CUR.execute(""" INSERT INTO judges(judge_name, pass_hash) VALUES (%(name)s, %(pwhash)s) """,
                    {'name': name, 'pwhash': pwhash})

        conn.commit()

    except:
        conn.rollback()
        raise ValueError("A judge with this name already exists.")


def add_competitor(first_name, last_name):
    """ check a competitor doesn't already exist and if not, add them """

    try:
        CUR.execute("""SELECT * FROM competitors WHERE competitor_first_name = %(first_name)s AND competitor_last_name = %(last_name)s""", {'first_name': first_name, 'last_name': last_name})
        
        rows = CUR.fetchall()

    except:
        conn.rollback()
        raise

    if len(rows) > 0:
        raise ValueError("A user with this name already exists.")
    
    try:
        CUR.execute("""INSERT INTO competitors (competitor_first_name, competitor_last_name) VALUES (%(first_name)s, %(last_name)s)""", {'first_name': first_name, 'last_name': last_name})
        conn.commit()
    
    except:
        conn.rollback()
        raise


def edit_competitor(competitor_id, first_name, last_name):
    """ check a competitor exists and edit them """

    try:
        CUR.execute("""SELECT * FROM competitors WHERE competitor_first_name = %(first_name)s AND competitor_last_name = %(last_name)s""", {'first_name': first_name, 'last_name': last_name})
        
        rows = CUR.fetchall()

    except:
        conn.rollback()
        raise

    if len(rows) > 0:
        raise ValueError("A user with this name already exists.")

    try:
        CUR.execute("""UPDATE competitors SET competitor_first_name = %(first_name)s, competitor_last_name = %(last_name)s WHERE competitor_id = %(competitor_id)s""", {'first_name': first_name, 'last_name': last_name, 'competitor_id': competitor_id})
        
        conn.commit()

    except:
        conn.rollback()
        raise