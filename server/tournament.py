from db import db_connect
from template4DoubleBracket import template4DoubleBracket
from template8DoubleBracket import template8DoubleBracket
from template16DoubleBracket import template16DoubleBracket
from template32DoubleBracket import template32DoubleBracket

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


def begin_new_tournament(tournament_id):
    bracket_object = {}
    rank_corresponding_match = {}

    try:
        CUR.execute(""" SELECT competitors.competitor_id, competitor_first_name, competitor_last_name FROM enrollment LEFT JOIN scores ON enrollment.competitor_id = scores.competitor_id JOIN competitors ON enrollment.competitor_id = competitors.competitor_id WHERE tournament_id = %(tournament_id)s GROUP BY competitors.competitor_id ORDER BY ROUND(AVG(total), 2) DESC """, {'tournament_id': tournament_id})
        competitors = CUR.fetchall()
        print(competitors)
        if (len(competitors) == 4):
            bracket_object = template4DoubleBracket
            rank_corresponding_match = {"0": 0, "1": 1, "2": 1, "3": 0}
        elif (len(competitors) <= 8):
            bracket_object = template8DoubleBracket
            rank_corresponding_match = {"0": 0, "1": 3, "2": 2, "3": 1, "4": 1, "5": 2, "6": 3, "7": 0}
        elif (len(competitors) <= 16):
            bracket_object = template16DoubleBracket
            rank_corresponding_match = {"0": 0, "1": 7, "2": 6, "3": 1, "4": 2, "5": 5, "6": 4, "7": 3, "8": 3, "9": 2, "10": 4, "11": 5, "12": 1, "13": 6, "14": 7, "15": 0}
        elif (len(competitors) <= 32):
            bracket_object = template32DoubleBracket
            rank_corresponding_match = {"0": 0, "1": 15, "2": 14, "3": 1, "4": 2, "5": 13, "6": 12, "7": 3, "8": 4, "9": 11, "10": 10, "11": 5, "12": 6, "13": 9, "14": 8, "15": 7, "16": 7, "17": 8, "18": 9, "19": 6, "20": 5, "21": 10, "22": 11, "23": 4, "24": 3, "25": 12, "26": 13, "27": 2, "28": 1, "29": 14, "30": 15, "31": 0}
        else:
            raise Exception
        for x in range(len(competitors)):
            match = rank_corresponding_match[str(x)]
            bracket_object["upper"][match]["participants"].append({"id": competitors[x][0], "name": f"{competitors[x][1]} {competitors[x][2]}"})
    except:
        conn.rollback()
        raise

    print(bracket_object)
    return bracket_object