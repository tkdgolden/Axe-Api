from db import db_connect

CUR, conn = db_connect()

def no_duplicate_lap(counter, quarter_id, discipline):
    """ checks if a lap already exists for that quarter """

    try:
        CUR.execute(""" SELECT * FROM laps WHERE counter = %(counter)s AND quarter_id = %(quarter_id)s AND discipline ILIKE %(discipline)s """, 
                    {'counter': counter,
                     'quarter_id': quarter_id,
                     'discipline': discipline})
        all_laps = CUR.fetchall()
    
    except:
        conn.rollback()
        raise

    if len(all_laps) < 1:
        return True
    else:
        return False


def add_lap(quarter_id, counter, discipline, start_date):
    """ adds a new lap """

    if not no_duplicate_lap(counter, quarter_id, discipline):
        raise ValueError("A similar lap already exists for the given quarter.")

    try:
        CUR.execute(""" INSERT INTO laps (quarter_id, counter, discipline, start_date) VALUES (%(quarter_id)s, %(counter)s, %(discipline)s, %(start_date)s) """, 
                    {'quarter_id': quarter_id,
                     'counter': counter,
                     'discipline': discipline,
                     'start_date': start_date})
        conn.commit()

    except:
        conn.rollback()
        raise