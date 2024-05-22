from db import db_connect

CUR, conn = db_connect()

def no_duplicate_competitor(first_name, last_name):
    """ check a competitor doesn't already exist """

    try:
        CUR.execute(""" SELECT * FROM competitors WHERE competitor_first_name = %(first_name)s AND competitor_last_name = %(last_name)s """, {'first_name': first_name, 'last_name': last_name})
        
        all_competitors = CUR.fetchall()

    except:
        conn.rollback()
        raise

    if len(all_competitors) > 0:
        raise ValueError("A competitor with this name already exists.")


def add_competitor(first_name, last_name):
    """  add a new competitor """

    try:
        no_duplicate_competitor(first_name, last_name)
    except:
        raise

    try:
        CUR.execute(""" INSERT INTO competitors (competitor_first_name, competitor_last_name) VALUES (%(first_name)s, %(last_name)s) RETURNING competitor_id """, {'first_name': first_name, 'last_name': last_name})
        conn.commit()
        competitor_id = CUR.fetchone()
    
    except:
        conn.rollback()
        raise
    return competitor_id


def edit_competitor(competitor_id, first_name, last_name):
    """ check a competitor exists and edit them """

    try:
        no_duplicate_competitor(first_name, last_name)
    except:
        raise

    try:
        CUR.execute(""" UPDATE competitors SET competitor_first_name = %(first_name)s, competitor_last_name = %(last_name)s WHERE competitor_id = %(competitor_id)s """, {'first_name': first_name, 'last_name': last_name, 'competitor_id': competitor_id})
        
        conn.commit()

    except:
        conn.rollback()
        raise


def get_all_competitors():
    try:
        CUR.execute(""" SELECT competitor_id, competitor_first_name, competitor_last_name FROM competitors """)
        competitors = CUR.fetchall()
    except:
        conn.rollback()
        raise
    return competitors


def get_competitors(competitor_name):
    try:
        CUR.execute(""" SELECT competitor_id, competitor_first_name, competitor_last_name FROM competitors WHERE ( competitor_first_name ILIKE %(competitor_name)s ) OR ( competitor_last_name ILIKE %(competitor_name)s ) """, {'competitor_name': competitor_name})
        competitors = CUR.fetchall()
    except:
        conn.rollback()
        raise
    return competitors