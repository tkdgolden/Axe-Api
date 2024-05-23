from db import db_connect

CUR, conn = db_connect()

def add_lap(season_id, discipline, start_date):
    """ adds a new lap """

    try:
        CUR.execute(""" INSERT INTO laps (season_id, discipline, start_date) VALUES (%(season_id)s, %(discipline)s, %(start_date)s) RETURNING lap_id, discipline, start_date """, 
                    {'season_id': season_id,
                     'discipline': discipline,
                     'start_date': start_date})
        conn.commit()
        new_lap_id = CUR.fetchone()

    except:
        conn.rollback()
        raise
    return new_lap_id


def get_lap_matches(lap_id):
    CUR.execute(""" SELECT * FROM matches """)
    print(CUR.fetchall())
    try:
        CUR.execute(""" SELECT match_id, player_1_id, player_2_id, dt FROM matches WHERE lap_id = %(lap_id)s """, {'lap_id': lap_id})
        matches = CUR.fetchall()
    except:
        conn.rollback()
        raise
    return matches