from db import db_connect

CUR, conn = db_connect()

def no_duplicate_quarter(month, season_id):
    """ checks if a quarter already exists for that season """

    try:
        CUR.execute(""" SELECT * FROM quarters WHERE month = %(month)s AND season_id = %(season_id)s """, 
                    {'season_id': season_id,
                     'month': month})
        all_quarters = CUR.fetchall()
    
    except:
        conn.rollback()
        raise

    if len(all_quarters) < 1:
        return True
    else:
        return False


def add_quarter(month, season_id, start_date):
    """ adds a new quarter """

    if not no_duplicate_quarter(month, season_id):
        raise ValueError("A similar quarter already exists for the given season.")

    try:
        CUR.execute(""" INSERT INTO quarters (month, season_id, start_date) VALUES (%(month)s, %(season_id)s, %(start_date)s) """, 
                    {'month': month,
                     'season_id': season_id,
                     'start_date': start_date})
        conn.commit()

    except:
        conn.rollback()
        raise