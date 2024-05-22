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


def get_all_seasons():
    try:
        CUR.execute(""" SELECT season_id, season, start_date FROM seasons ORDER BY start_date DESC """)
        all_seasons = CUR.fetchall()
        print(all_seasons)
    except:
        conn.rollback()
        raise
    return all_seasons

def get_season_info(season_id):
    try:
        CUR.execute(""" SELECT season, start_date FROM seasons WHERE season_id = %(season_id)s """, {'season_id': season_id})
        season = CUR.fetchone()
        CUR.execute(""" SELECT lap_id, discipline, start_date FROM laps WHERE season_id = %(season_id)s """, {'season_id': season_id})
        laps = CUR.fetchall()
        CUR.execute(""" SELECT competitors.competitor_id, competitor_first_name, competitor_last_name FROM enrollment JOIN competitors ON competitors.competitor_id = enrollment.competitor_id WHERE season_id = %(season_id)s """, {'season_id': season_id})
        competitors = CUR.fetchall()
        print("competitors", competitors)
        print(laps)
        print(season)
        print(competitors)
    except:
        conn.rollback()
        raise
    return [season, laps, competitors]