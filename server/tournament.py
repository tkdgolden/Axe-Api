from db import db_connect

CUR, conn = db_connect()

possible_scores = [0, 1, 2, 3, 4, 6, 12]

bracket_E_seed_order = [0, 3, 1, 2]
bracket_H_seed_order = [0, 7, 3, 4, 2, 5, 1, 6]
bracket_K_seed_order = [0, 15, 7, 8, 3, 12, 4, 11, 1, 14, 6, 9, 2, 13, 5, 10]
bracket_N_seed_order = [0, 31, 15, 16, 8, 23, 7, 24, 3, 28, 12, 19, 11, 20, 4, 27, 1, 30, 14, 17, 9, 22, 6, 25, 2, 29, 13, 18, 10, 21, 5, 26]

bracket_F_seed_order = [1, 2, 0, 3]
bracket_I_seed_order = [3, 4, 2, 5, 1, 6, 0, 7]


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


def begin_new_tournament(tournament_id):

    try:
        CUR.execute(""" SELECT competitors.competitor_id FROM enrollment LEFT JOIN scores ON enrollment.competitor_id = scores.competitor_id JOIN competitors ON enrollment.competitor_id = competitors.competitor_id WHERE tournament_id = %(tournament_id)s GROUP BY competitors.competitor_id ORDER BY ROUND(AVG(total), 2) DESC """, {'tournament_id': tournament_id})
        competitors = CUR.fetchall()
        print(competitors)

    except:
        conn.rollback()
        raise

    if (len(competitors) < 4 or len(competitors) > 64):
        raise Exception
        
    try:
        create_first_round(competitors, tournament_id)
    except:
        conn.rollback()
        raise

    try:
        CUR.execute(""" UPDATE tournaments SET enrollment_open = FALSE WHERE tournament_id = %(tournament_id)s """, {'tournament_id': tournament_id})
    except:
        conn.rollback()
        raise
        
    return True


def create_first_round(competitor_list, tournament_id):
    seed_order = []
    which_round = ""
    bye_array = []
    matches_array = []

    if (len(competitor_list) == 4):
        seed_order = bracket_E_seed_order
        which_round = "E"
    elif (len(competitor_list) <= 8):
        seed_order = bracket_H_seed_order
        which_round = "H"
    elif (len(competitor_list) <= 16):
        seed_order = bracket_K_seed_order
        which_round = "K"
    elif (len(competitor_list) <= 32):
        seed_order = bracket_N_seed_order
        which_round = "N"

    competitor_one = None
    competitor_two = None
    for each in seed_order:
        match_id = None
        if competitor_one is None:
            competitor_one = competitor_list[each]["competitor_id"]
        else:
            if competitor_list[each]:
                competitor_two = competitor_list[each]["competitor_id"]
                try:
                    CUR.execute(""" INSERT INTO matches (player_1_id, player_2_id, tournament_id) VALUES (%(player_one)s, %(player_two)s, %(tournament_id)s) RETURNING match_id """, {'player_one': competitor_one, 'player_two': competitor_two, 'tournament_id': tournament_id})
                    conn.commit()
                    match_id = CUR.fetchone()[0]
                except:
                    conn.rollback()
                    raise
                bye_array.append(0)
                matches_array.append(match_id)
            else:
                bye_array.append(competitor_one)
            competitor_one = None
            competitor_two = None
    
    try:
        CUR.execute(""" INSERT INTO rounds (tournament_id, matches, bye_competitors, which_round) VALUES (%(tournament_id)s, %(matches_array)s, %(bye_array)s, %(which_round)s) RETURNING round_id """, {'tournament_id': tournament_id, 'matches_array': matches_array, 'bye_array': bye_array, 'which_round': which_round})
        conn.commit()
        round_id = CUR.fetchone()[0]
    except:
        conn.rollback()
        raise

    try:
        CUR.execute(""" UPDATE tournaments SET current_round = %(round_id)s WHERE tournament_id = %(tournament_id)s """, {'round_id': round_id, 'tournament_id': tournament_id})
        conn.commit()
    except:
        conn.rollback()
        raise


def create_simple_round(competitor_list, tournament_id, which_round):

    bye_array = []
    matches_array = []
    competitor_one = None
    competitor_two = None
    for each in competitor_list:
        match_id = None
        if competitor_one is None:
            if each is None:
                competitor_one = "skip"
            else:
                competitor_one = each
        else:
            if each is None:
                if competitor_one != "skip":
                    bye_array.append(competitor_one)
            else:
                competitor_two = each
                try:
                    CUR.execute(""" INSERT INTO matches (player_1_id, player_2_id, tournament_id) VALUES (%(player_one)s, %(player_two)s, %(tournament_id)s) RETURNING match_id """, {'player_one': competitor_one, 'player_two': competitor_two, 'tournament_id': tournament_id})
                    conn.commit()
                    match_id = CUR.fetchone()[0]
                except:
                    conn.rollback()
                    raise
                bye_array.append(0)
                matches_array.append(match_id)
            competitor_one = None
            competitor_two = None

    try:
        CUR.execute(""" INSERT INTO rounds (tournament_id, matches, bye_competitors, which_round) VALUES (%(tournament_id)s, %(matches_array)s, %(bye_array)s, %(which_round)s) RETURNING round_id """, {'tournament_id': tournament_id, 'matches_array': matches_array, 'bye_array': bye_array, 'which_round': which_round})
        conn.commit()
        round_id = CUR.fetchone()[0]
    except:
        conn.rollback()
        raise

    try:
        CUR.execute(""" UPDATE tournaments SET current_round = %(round_id)s WHERE tournament_id = %(tournament_id)s """, {'round_id': round_id, 'tournament_id': tournament_id})
        conn.commit()
    except:
        conn.rollback()
        raise


def create_F_I_round(competitor_list, tournament_id, which_round):
    seed_order = []
    bye_array = []
    matches_array = []
    
    if (which_round == "F"):
        seed_order = bracket_F_seed_order
    else:
        seed_order = bracket_I_seed_order

    competitor_one = None
    competitor_two = None
    for each in seed_order:
        match_id = None
        if competitor_one is None:
            competitor_one = competitor_list[each]
        else:
            if competitor_list[each]:
                competitor_two = competitor_list[each]
                try:
                    CUR.execute(""" INSERT INTO matches (player_1_id, player_2_id, tournament_id) VALUES (%(player_one)s, %(player_two)s, %(tournament_id)s) RETURNING match_id """, {'player_one': competitor_one, 'player_two': competitor_two, 'tournament_id': tournament_id})
                    conn.commit()
                    match_id = CUR.fetchone()[0]
                except:
                    conn.rollback()
                    raise
                bye_array.append(0)
                matches_array.append(match_id)
            else:
                bye_array.append(competitor_one)
            competitor_one = None
            competitor_two = None
    
    try:
        CUR.execute(""" INSERT INTO rounds (tournament_id, matches, bye_competitors, which_round) VALUES (%(tournament_id)s, %(matches_array)s, %(bye_array)s, %(which_round)s) RETURNING round_id """, {'tournament_id': tournament_id, 'matches_array': matches_array, 'bye_array': bye_array, 'which_round': which_round})
        conn.commit()
        round_id = CUR.fetchone()[0]
    except:
        conn.rollback()
        raise

    try:
        CUR.execute(""" UPDATE tournaments SET current_round = %(round_id)s WHERE tournament_id = %(tournament_id)s """, {'round_id': round_id, 'tournament_id': tournament_id})
        conn.commit()
    except:
        conn.rollback()
        raise