from db import db_connect

CUR, conn = db_connect()

def no_duplicate_season(season, start_date):
    """ checks if a season already exists for that year """

    year = start_date.year
    next_year = year + 1

    try:
        CUR.execute(""" SELECT * FROM seasons WHERE season = %(season)s AND start_date BETWEEN '%(year)s-01-01 00:00:00'::timestamp AND '%(next_year)s-01-01 00:00:00'::timestamp """, 
                    {'season': season,
                     'year': year,
                     'next_year': next_year})
        all_seasons = CUR.fetchall()
    
    except:
        conn.rollback()
        raise

    if len(all_seasons) < 1:
        return True
    else:
        return False


def add_season(season, start_date):
    """ adds a new season """

    if not no_duplicate_season(season, start_date):
        raise ValueError("A similar season already exists for the given year.")

    try:
        CUR.execute(""" INSERT INTO seasons (season, start_date) VALUES (%(season)s, %(start_date)s) """, 
                    {'season': season, 'start_date': start_date})
        conn.commit()

    except:
        conn.rollback()
        raise