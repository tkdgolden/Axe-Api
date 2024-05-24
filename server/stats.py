from db import db_connect
from template4DoubleBracket import template4DoubleBracket
from template8DoubleBracket import template8DoubleBracket
from template16DoubleBracket import template16DoubleBracket
from template32DoubleBracket import template32DoubleBracket

rounds_to_matches = {
    "A": [1],
    "B": [2],
    "C": [3],
    "D": [4],
    "E": [5, 6],
    "F": [7, 8],
    "G": [9, 10],
    "H": [11, 12, 13, 14],
    "I": [15, 16, 17, 18],
    "J": [19, 20, 21, 22],
    "K": [23, 24, 25, 26, 27, 28, 29, 30],
    "L": [31, 32, 33, 34, 35, 36, 37, 38],
    "M": [39, 40, 41, 42, 43, 44, 45, 46],
    "N": [47, 48, 49, 50, 51, 52, 53, 54]
}

upper_rounds = ["A", "B", "E", "H", "K", "N"]

CUR, conn = db_connect()

def get_overall_stats():
    """ all player stats selects from all scores """

    try:
        CUR.execute(""" SELECT competitor_id, competitor_first_name || ' ' || competitor_last_name full_name, ROUND(AVG(total), 2), COUNT(win), COUNT(score_id), MAX(total), MIN(total) FROM scores JOIN competitors USING (competitor_id) JOIN matches ON scores.match_id = matches.match_id WHERE matches.discipline ILIKE 'hatchet' GROUP BY competitor_id, full_name ORDER BY full_name """)
        all_stats = CUR.fetchall()

    except:
        conn.rollback()
        raise

    print(all_stats)
    return all_stats


def get_season_stats(season_id):
    try:
        CUR.execute(""" SELECT competitors.competitor_id, competitor_first_name || ' ' || competitor_last_name full_name, ROUND(AVG(total), 2), COUNT(win), COUNT(score_id), MAX(total), MIN(total) FROM scores JOIN matches ON scores.match_id = matches.match_id JOIN laps ON matches.lap_id = laps.lap_id JOIN seasons ON laps.season_id = seasons.season_id JOIN competitors ON scores.competitor_id = competitors.competitor_id WHERE seasons.season_id = %(season_id)s GROUP BY competitors.competitor_id, full_name ORDER BY full_name  """, {'season_id': season_id})
        season_stats = CUR.fetchall()
        print(season_stats)
    except:
        conn.rollback()
        raise
    return season_stats


def get_discipline_stats(discipline):
    try:
        CUR.execute(""" SELECT competitors.competitor_id, competitor_first_name || ' ' || competitor_last_name full_name, ROUND(AVG(total), 2), COUNT(win), COUNT(score_id), MAX(total), MIN(total) FROM scores JOIN matches ON scores.match_id = matches.match_id JOIN competitors USING (competitor_id) WHERE matches.discipline ILIKE %(discipline)s GROUP BY competitors.competitor_id, full_name ORDER BY full_name  """, {'discipline': discipline})
        discipline_stats = CUR.fetchall()
        print(discipline_stats)
    except:
        conn.rollback()
        raise
    return discipline_stats


def get_competitor_stats(competitor_id):
    try:
        CUR.execute(""" SELECT competitor_id, competitor_first_name, competitor_last_name, ROUND(AVG(total), 2), COUNT(win), COUNT(score_id), MAX(total), MIN(total) FROM scores JOIN matches ON scores.match_id = matches.match_id JOIN competitors USING (competitor_id) WHERE competitors.competitor_id = %(competitor_id)s GROUP BY competitor_id, competitor_first_name, competitor_last_name, discipline """, {'competitor_id': competitor_id})
        competitor_stats = CUR.fetchall()
        print(competitor_stats)
    except:
        conn.rollback()
        raise
    return competitor_stats


def get_tournament_stats(tournament_id):
    bracket_object = {}

    try:
        CUR.execute(""" SELECT * FROM rounds WHERE tournament_id = %(tournament_id)s ORDER BY which_round DESC """, {'tournament_id': tournament_id})
        rounds = CUR.fetchall()
    except:
        conn.rollback()
        raise

    try:
        CUR.execute(""" SELECT match_id, p1.competitor_first_name || ' ' || p1.competitor_last_name as player1, player_1_id, player_1_total, p2.competitor_first_name || ' ' || p2.competitor_last_name as player2, player_2_id, player_2_total, winner_id FROM matches JOIN competitors p1 ON p1.competitor_id = matches.player_1_id JOIN competitors p2 ON p2.competitor_id = matches.player_2_id WHERE tournament_id = %(tournament_id)s """, {'tournament_id': tournament_id})
        matches = CUR.fetchall()
    except:
        conn.rollback()
        raise

    if rounds[0]["which_round"] == "E":
        bracket_object = template4DoubleBracket
    elif rounds[0]["which_round"] == "H":
        bracket_object = template8DoubleBracket
    elif rounds[0]["which_round"] == "K":
        bracket_object = template16DoubleBracket
    elif rounds[0]["which_round"] == "N":
        bracket_object = template32DoubleBracket
    else:
        raise Exception

    for round in rounds:
        which_round = round["which_round"]
        match_locations = rounds_to_matches[which_round]
        potential_match_list = []
        if which_round in upper_rounds:
            potential_match_list = bracket_object["upper"]
            for match_count in range(len(match_locations)):
                for potential_index in range(len(potential_match_list)):
                    if potential_match_list[potential_index]["id"] == match_locations[match_count]:
                        match_id = round["matches"][match_count]
                        match = []
                        for each in matches:
                            if each["match_id"] == match_id:
                                match = each
                                bracket_object["upper"][match_count]["participants"] = [
                                    {
                                        "id": match["player_1_id"],
                                        "name": match["player1"],
                                        "resultText": match["player_1_total"],
                                        "isWinner": (match["winner_id"] == match["player_1_id"])
                                    },
                                    {
                                        "id": match["player_2_id"],
                                        "name": match["player2"],
                                        "resultText": match["player_2_total"],
                                        "isWinner": (match["winner_id"] == match["player_2_id"])
                                    }
                                ]
        else:
            potential_match_list = bracket_object["lower"]

    print(bracket_object)
    return(bracket_object)