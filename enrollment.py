from db import db_connect

CUR, conn = db_connect()

def no_duplicate_enrollment(competitor_id, tournament_id = None, season_id = None):
    """ checks if a enrollment already exists for that competitor and season or tournament """

    if season_id:
        try:
            CUR.execute(""" SELECT * FROM enrollment WHERE competitor_id = %(competitor_id)s AND season_id = %(season_id)s """, 
                        {'competitor_id': competitor_id,
                         'season_id': season_id})
            already_enrolled = CUR.fetchall()
        except:
            conn.rollback()
            raise

    elif tournament_id:
        try:
            CUR.execute(""" SELECT * FROM enrollment WHERE competitor_id = %(competitor_id)s AND tournament_id = %(tournament_id)s """, 
                        {'competitor_id': competitor_id,
                         'tournament_id': tournament_id})
            already_enrolled = CUR.fetchall()
        except:
            conn.rollback()
            raise
    else:
        raise ValueError("Must verify a season or tournament.")
    
    if len(already_enrolled) > 0:
        return False
    else:
        return True


def add_enrollment(competitor_id, tournament_id = None, season_id = None):
    """ enrolls a competitor in a season or tournament """

    if not no_duplicate_enrollment(competitor_id, tournament_id, season_id):
        raise ValueError("This competitor is already enrolled.")

    if season_id:
        try:
            CUR.execute(""" INSERT INTO enrollment (season_id, competitor_id) VALUES (%(season_id)s, %(competitor_id)s) """, 
                        {'season_id': season_id,
                        'competitor_id': competitor_id})
            conn.commit()

        except:
            conn.rollback()
            raise

    elif tournament_id:
        try:
            CUR.execute(""" INSERT INTO enrollment (tournament_id, competitor_id) VALUES (%(tournament_id)s, %(competitor_id)s) """, 
                        {'tournament_id': tournament_id,
                        'competitor_id': competitor_id})
            conn.commit()

        except:
            conn.rollback()
            raise
    else:
        raise ValueError("Must specify a season or tournament.")