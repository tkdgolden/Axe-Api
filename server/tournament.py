from db import db_connect

CUR, conn = db_connect()


def no_duplicate_tournament(tournament_name, discipline, tournament_date):
    """ checks if a tournament already exists """

    try:
        CUR.execute(""" SELECT * FROM tournaments WHERE tournament_name ILIKE %(tournament_name)s AND discipline ILIKE %(discipline)s AND tournament_date = %(tournament_date)s """, 
                    {'tournament_name': tournament_name,
                     'discipline': discipline,
                     'tournament_date': tournament_date})
        all_tournaments = CUR.fetchall()
    except:
        conn.rollback()
        raise
    
    if len(all_tournaments) > 0:
        return False
    else:
        return True


def add_tournament(tournament_name, discipline, tournament_date):
    """ adds a new tournament """

    if not no_duplicate_tournament(tournament_name, discipline, tournament_date):
        raise ValueError("A similar tournament already exists.")

    try:
        CUR.execute(""" INSERT INTO tournaments (tournament_name, discipline, tournament_date) VALUES (%(tournament_name)s, %(discipline)s, %(tournament_date)s) """, 
                    {'tournament_name': tournament_name,
                     'discipline': discipline,
                     'tournament_date': tournament_date})
        conn.commit()

    except:
        conn.rollback()
        raise


def update_tournament_enrollment(tournament_id):
    """ sets tournament's enrollment to false """

    try:
        CUR.execute(""" UPDATE tournaments SET enrollment_open = FALSE WHERE tournament_id = %(tournament_id)s """,
                    {'tournament_id': tournament_id})
        conn.commit()
    
    except:
        conn.rollback()
        raise


def update_tournament_current_round(tournament_id, round_id):
    """ sets tournament's current round """

    try:
        CUR.execute(""" UPDATE tournaments SET current_round = %(round_id)s WHERE tournament_id = %(tournament_id)s """,
                    {'round_id': round_id,
                     'tournament_id': tournament_id})
        conn.commit()
        
    except:
        conn.rollback()
        raise


def get_all_tournaments():
    try:
        CUR.execute(""" SELECT tournament_id, tournament_name, tournament_date FROM tournaments ORDER BY tournament_date """)
        all_tournaments = CUR.fetchall()
        print(all_tournaments)
    except:
        conn.rollback()
        raise
    return all_tournaments