import psycopg2
import psycopg2.extras
from werkzeug.security import generate_password_hash, check_password_hash

def db_connect():
    global conn
    conn = psycopg2.connect("dbname=test_axe")

    global CUR
    CUR = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    return CUR

def add_judge(name, password):
    """ hash password, create new judge """

    try:
        pwhash = generate_password_hash(password)

        CUR.execute(""" INSERT INTO judges(judge_name, pass_hash) VALUES (%(name)s, %(pwhash)s) """,
                    {'name': name, 'pwhash': pwhash})

        conn.commit()

    except:
        conn.rollback()
        raise ValueError("A judge with this name already exists.")
    

def verify_judge(name, password):
    """ verify's judge name and hashed password match """

    try:
        CUR.execute(""" SELECT * FROM judges WHERE judge_name = %(name)s """, 
                    {'name': name})
        all_judges = CUR.fetchall()

    except:
        conn.rollback()
        raise

    if len(all_judges) != 1:
        raise ValueError("The judge name was not found.")
    
    pass_hash = all_judges[0]["pass_hash"]
    
    if not check_password_hash(pass_hash, password):
        raise ValueError("The password didn't match.")
    else:
        # a more efficient, readable way to unpack this? vvv
        return all_judges[0]["judge_id"], all_judges[0]["judge_name"]


def no_duplicate_competitor(first_name, last_name):
    """ check a competitor doesn't already exist """

    try:
        CUR.execute(""" SELECT * FROM competitors WHERE competitor_first_name = %(first_name)s AND competitor_last_name = %(last_name)s """, {'first_name': first_name, 'last_name': last_name})
        
        all_competitors = CUR.fetchall()

    except:
        conn.rollback()
        raise

    if len(all_competitors) > 0:
        raise ValueError("A user with this name already exists.")


def add_competitor(first_name, last_name):
    """  add a new competitor """

    try:
        no_duplicate_competitor(first_name, last_name)
    except:
        raise

    try:
        CUR.execute(""" INSERT INTO competitors (competitor_first_name, competitor_last_name) VALUES (%(first_name)s, %(last_name)s) """, {'first_name': first_name, 'last_name': last_name})
        conn.commit()
    
    except:
        conn.rollback()
        raise


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


def no_duplicate_lap(counter, quarter_id, discipline):
    """ checks if a lap already exists for that quarter """

    try:
        CUR.execute(""" SELECT * FROM laps WHERE counter = %(counter)s AND quarter_id = %(quarter_id)s AND discipline ILIKE %(discipline)s """, 
                    {'counter': counter,
                     'quarter_id': quarter_id,
                     'discipline': discipline})
        all_laps = CUR.fetchall()
    
    except:
        conn.rollback()
        raise

    if len(all_laps) < 1:
        return True
    else:
        return False


def add_lap(quarter_id, counter, discipline, start_date):
    """ adds a new lap """

    if not no_duplicate_lap(counter, quarter_id, discipline):
        raise ValueError("A similar lap already exists for the given quarter.")

    try:
        CUR.execute(""" INSERT INTO laps (quarter_id, counter, discipline, start_date) VALUES (%(quarter_id)s, %(counter)s, %(discipline)s, %(start_date)s) """, 
                    {'quarter_id': quarter_id,
                     'counter': counter,
                     'discipline': discipline,
                     'start_date': start_date})
        conn.commit()

    except:
        conn.rollback()
        raise


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
    
    except:
        conn.rollback()
        raise


def update_tournament_current_round(tournament_id, round_id):
    """ sets tournament's current round """

    try:
        CUR.execute(""" UPDATE tournaments SET current_round = %(round_id)s WHERE tournament_id = %(tournament_id)s """,
                    {'round_id': round_id,
                     'tournament_id': tournament_id})
        
    except:
        conn.rollback()
        raise


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
        CUR.execute(""" INSERT INTO matches (player_1_id, player_2_id, lap_id) VALUES (%(player_1_id)s, %(player_2_id)s, %(lap_id)s) """,
                    {'player_1_id': player_1_id,
                     'player_2_id': player_2_id,
                     'lap_id': lap_id})
        conn.commit()

    except:
        conn.rollback()
        raise


def update_completed_match(match_id, winner_id, discipline, judge_id, dt, player_1_total, player_2_total):
    """ updates a match with complete data """

    try:
        CUR.execute(""" UPDATE matches SET winner_id = %(winner_id)s,  discipline = %(discipline)s, judge_id = %(judge_id)s, dt = %(dt)s, player_1_total = %(player_1_total)s,  player_2_total = %(player_2_total)s WHERE match_id = %(match_id)s """,
                    {'winner_id': winner_id,
                     'discipline': discipline,
                     'judge_id': judge_id,
                     'dt': dt,
                     'player_1_total': player_1_total,
                     'player_2_total': player_2_total,
                     'match_id': match_id})
        conn.commit()

    except:
        conn.rollback()
        raise