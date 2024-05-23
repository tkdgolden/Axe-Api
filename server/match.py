from db import db_connect

CUR, conn = db_connect()


def add_unscored_tournament_match(player_1_id, player_2_id, tournament_id):
    """ adds an empty tournament match """

    try:
        CUR.execute(""" INSERT INTO matches (player_1_id, player_2_id, tournament_id) VALUES (%(player_1_id)s, %(player_2_id)s, %(tournament_id)s) """,
                    {'player_1_id': player_1_id,
                     'player_2_id': player_2_id,
                     'tournament_id': tournament_id})
        conn.commit()

    except:
        conn.rollback()
        raise


def add_unscored_season_match(player_1_id, player_2_id, lap_id):
    """ adds an empty season match to given lap """

    try:
        CUR.execute(""" INSERT INTO matches (player_1_id, player_2_id, lap_id) VALUES (%(player_1_id)s, %(player_2_id)s, %(lap_id)s) RETURNING match_id """,
                    {'player_1_id': player_1_id,
                     'player_2_id': player_2_id,
                     'lap_id': lap_id})
        conn.commit()
        match_id = CUR.fetchone()
    except:
        conn.rollback()
        raise
    return match_id


def update_completed_match(match_id, winner_id, judge_id, dt, player_1_total, player_2_total):
    """ updates a match with complete data """

    try:
        CUR.execute(""" UPDATE matches SET winner_id = %(winner_id)s, discipline = (SELECT discipline FROM laps JOIN matches ON laps.lap_id = matches.lap_id WHERE match_id = %(match_id)s), judge_id = %(judge_id)s, dt = %(dt)s, player_1_total = %(player_1_total)s,  player_2_total = %(player_2_total)s WHERE match_id = %(match_id)s """,
                    {'winner_id': winner_id,
                     'judge_id': judge_id,
                     'dt': dt,
                     'player_1_total': player_1_total,
                     'player_2_total': player_2_total,
                     'match_id': match_id})
        conn.commit()

    except:
        conn.rollback()
        raise


def get_match(match_id):
    try:
        CUR.execute(""" SELECT p1.competitor_first_name || ' ' || p1.competitor_last_name as player1, p2.competitor_first_name || ' ' || p2.competitor_last_name as player2 FROM matches JOIN competitors p1 ON p1.competitor_id = matches.player_1_id JOIN competitors p2 ON p2.competitor_id = matches.player_2_id WHERE match_id = %(match_id)s """, {'match_id': match_id})
        match_info = CUR.fetchone()
    except:
        conn.rollback()
        raise
    return match_info