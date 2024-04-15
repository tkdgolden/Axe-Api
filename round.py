from db import db_connect

CUR, conn = db_connect()


def add_round(tournament_id, matches_array, bye_array, which_round):
    """ adds a new round for a tournament """

    try:
        CUR.execute(""" INSERT INTO rounds (tournament_id, matches, bye_competitors, which_round) VALUES (%(tournament_id)s, %(matches_array)s, %(bye_array)s, %(which_round)s) """, 
                    {'tournament_id': tournament_id,
                     'matches_array': matches_array,
                     'bye_array': bye_array,
                     'which_round': which_round})
        conn.commit()

    except:
        conn.rollback()
        raise