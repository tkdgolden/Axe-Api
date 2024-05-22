from datetime import datetime, date
from flask import Flask, jsonify, request, session, json, make_response
import jwt
from db import *
from auth import login_required, SECRET_KEY
from judge import *
from competitor import *
from season import *
from lap import *
from enrollment import *
from tournament import *
from round import *
from match import *
from score import *
import os
from flask_cors import CORS
from stats import *

app = Flask(__name__)
app.secret_key = SECRET_KEY

db_connect()
CORS(app, supports_credentials=True)


@app.route("/judges/new", methods=["POST"])
@login_required
def new_judge():
    """ create a new judge """

    try:
        name = request.json["name"]
        password = request.json["password"]
    except:
        error = "A new judge requires a name and password."
        print(error)
        return jsonify(error), 400

    try:
        add_judge(name, password)
        return jsonify(success = True), 201
    except Exception as error:
        print(error)
        return jsonify(error = str(error)), 400


@app.route("/judges/verify", methods=["POST"])
def check_judge():
    """ verify a judge """

    try:
        name = request.json["name"]
        password = request.json["password"]
    except:
        error = "A judge requires a name and password."
        print(error)
        return jsonify(error), 400

    try:
        judge_id = verify_judge(name, password)
        token = jwt.encode({'user_id': judge_id}, SECRET_KEY, algorithm='HS256')
        return jsonify({'token': token})
    except Exception as error:
        print(error)
        return jsonify(error = str(error)), 400
    


@app.route('/competitors', methods=["POST", "PUT"])
@login_required
def competitor():
    """ create or edit competitor """

    try:
        first_name = request.json["first_name"]
        last_name = request.json["last_name"]
    except:
        error = "A new competitor requires a first and last name."
        print(error)
        return jsonify(error), 400

    if request.method == 'POST':
        """ create a new competitor """
        
        try:
            new_competitor = add_competitor(first_name, last_name)
            return jsonify(new_competitor), 201
        except Exception as error:
            print(error)
            return jsonify(error = str(error)), 400
        
    if request.method == 'PUT':
        """ replace an existing competitor """
        
        try:
            competitor_id = request.json["competitor_id"]
        except:
            error = "A competitor requires an id to edit."
            print(error)
            return jsonify(error), 400

        try:
            edit_competitor(competitor_id, first_name, last_name)
            return jsonify(success=True)
        except Exception as error:
            print(error)
            return jsonify(error = str(error)), 400
        

@app.route('/seasons', methods=["POST"])
@login_required
def season():
    """ create a new season """

    try:
        season = request.json["season"]
        start_date = datetime.strptime(request.json["start_date"], '%Y-%m-%d')
    except:
        error = "A new season requires a season and start date."
        print(error)
        return jsonify(error), 400
    
    try:
        add_season(season, start_date)
        return jsonify(success=True), 201
    except Exception as error:
        print(error)
        return jsonify(error = str(error)), 400
    

@app.route("/seasons/<season_id>")
def season_info(season_id):
    print("season info", season_id)
    try:
        [season, laps, competitors] = get_season_info(season_id)
        return jsonify([season, laps, competitors])
    except Exception as error:
        print(error)
        return jsonify(error = str(error)), 400
    

@app.route('/laps', methods=["POST"])
@login_required
def lap():
    """ create a new lap """
    print("here")
    try:
        season_id = request.json["season_id"]
        discipline = request.json["discipline"]
        start_date = date.today()
    except:
        error = "A new lap requires a season id and discipline."
        print(error)
        return jsonify(error), 400
    
    try:
        new_lap_id = add_lap(season_id, discipline, start_date)
        return jsonify(new_lap_id), 201
    except Exception as error:
        print(error)
        return jsonify(error = str(error)), 400
    

@app.route('/laps/<lap_id>')
def lap_matches(lap_id):
    try:
        matches = get_lap_matches(int(lap_id))
        return jsonify(matches)
    except Exception as error:
        print(error)
        return jsonify(error = str(error)), 400
    

@app.route('/enrollment', methods=["POST"])
@login_required
def enrollment():
    """ enrolls a competitor to a season or tournament """

    try:
        competitor_id = request.json["competitor_id"]
        season_id = request.json["season_id"] or None
        tournament_id = request.json["tournament_id"] or None
        print(competitor_id)
        print(season_id)
        print(tournament_id)
    except:
        error = "Enrollment requires a competitor id and either a season id or a tournament id."
        print(error)
        return jsonify(error), 400
    
    try:
        add_enrollment(competitor_id, season_id, tournament_id)
        return jsonify(success=True), 201
    except Exception as error:
        print(error)
        return jsonify(error = str(error)), 400
    

@app.route('/tournaments', methods=["POST"])
@login_required
def tournaments():
    """ adds a new tournament """

    try:
        tournament_name = request.json["name"]
        discipline = request.json["discipline"]
        tournament_date = request.json["date"]
    except:
        error = "A new tournament requires a name, discipline and date."
        print(error)
        return jsonify(error), 400
    
    try:
        add_tournament(tournament_name, discipline, tournament_date)
        return jsonify(success=True), 201
    except Exception as error:
        print(error)
        return jsonify(error = str(error)), 400
    

@app.route('/tournaments/<tournament_id>/begin')
def begin_tournament(tournament_id):
    try:
        bracket_object = begin_new_tournament(tournament_id)
        return jsonify(bracket_object)
    except Exception as error:
        print(error)
        return jsonify(error = str(error)), 400
    

@app.route('/rounds', methods=["POST"])
@login_required
def rounds():
    """ adds a new round """

    try:
        tournament_id = request.json["tournament_id"]
        matches_array = request.json["matches_array"]
        bye_array = request.json["bye_array"]
        which_round = request.json["which_round"]
    except:
        error = "A new round requires a tournament id, matches array, bye array, and which round."
        print(error)
        return jsonify(error), 400
    
    try:
        add_round(tournament_id, matches_array, bye_array, which_round)
        return jsonify(success=True), 201
    except Exception as error:
        print(error)
        return jsonify(error = str(error)), 400
    

@app.route('/matches', methods=["POST"])
@login_required
def add_matches():
    """ adds a new match """
    
    try:
        player_1_id = request.json["player_1_id"]
        player_2_id = request.json["player_2_id"]

        if ("lap_id" in request.json and "tournament_id" in request.json):
            raise
        elif ("lap_id" in request.json):
            lap_id = request.json["lap_id"]
            tournament_id = None
        elif ("tournament_id" in request.json):
            tournament_id = request.json["tournament_id"]
            lap_id = None
        else:
            raise
    except:
        error = "A new match requires a plaery 1 id, player 2 id, and either a tournament id or lap id."
        print(error)
        return jsonify(error), 400
    
    try:
        if (lap_id):
            add_unscored_season_match(player_1_id, player_2_id, lap_id)
        elif (tournament_id):
            add_unscored_tournament_match(player_1_id, player_2_id, tournament_id)
        return jsonify(success=True), 201
    except Exception as error:
        print(error)
        return jsonify(error = str(error)), 400
    

@app.route('/matches/<match_id>', methods=["PATCH"])
@login_required
def finish_matches(match_id):
    """ updates a completed match """
    
    try:
        winner_id = request.json["winner_id"]
        discipline = request.json["discipline"]
        judge_id = request.json["judge_id"]
        dt = request.json["dt"]
        player_2_total = request.json["player_2_total"]
        player_1_total = request.json["player_1_total"]
    except:
        error = "A completed match requires a match id, winner id, discipline, judge id, date/time, and totals for both players."
        print(error)
        return jsonify(error), 400
    
    try:
        update_completed_match(match_id, winner_id, discipline, judge_id, dt, player_1_total, player_2_total)
        return jsonify(success=True), 201
    except Exception as error:
        print(error)
        return jsonify(error = str(error)), 400
    

@app.route('/scores', methods=["POST"])
@login_required
def add_scores():
    """ adds a new score """
    
    try:
        competitor_id = request.json["competitor_id"]
        match_id = request.json["match_id"]
        quick_points = request.json["quick_points"]
        sequence = request.json["sequence"]
        throw1 = request.json["throw1"]
        throw2 = request.json["throw2"]
        throw3 = request.json["throw3"]
        throw4 = request.json["throw4"]
        throw5 = request.json["throw5"]
        throw6 = request.json["throw6"]
        throw7 = request.json["throw7"]
        throw8 = request.json["throw8"]
        total = request.json["total"]
        win = request.json["win"]
    except:
        error = "A new score requires a competitor id, match id, quick points, sequence, scores for each of 8 throws, a total, and if the player won or not."
        print(error)
        return jsonify(error), 400
    
    try:
        add_player_score(competitor_id, match_id, quick_points, sequence, throw1, throw2, throw3, throw4, throw5, throw6, throw7, throw8, total, win)
        return jsonify(success=True), 201
    except Exception as error:
        print(error)
        return jsonify(error = str(error)), 400
    

@app.route("/scores/all")
def overall_stats():
    try:
        stats = get_overall_stats()
        return jsonify(stats)
    except Exception as error:
        print(error)
        return jsonify(error = str(error)), 400
    

@app.route("/seasons/all")
def all_seasons():
    try:
        seasons = get_all_seasons()
        return jsonify(seasons)
    except Exception as error:
        print(error)
        return jsonify(error = str(error)), 400
    

@app.route("/tournaments/all")
def all_tournaments():
    try:
        tournaments = get_all_tournaments()
        return jsonify(tournaments)
    except Exception as error:
        print(error)
        return jsonify(error = str(error)), 400
    

@app.route("/competitors/all")
def all_competitors():
    try:
        competitors = get_all_competitors()
        return jsonify(competitors)
    except Exception as error:
        print(error)
        return jsonify(error = str(error)), 400
    

@app.route("/competitors/<competitor_name>")
def find_competitor(competitor_name):
    try:
        search_name = "%" + competitor_name + "%"
        competitors = get_competitors(search_name)
        return jsonify(competitors)
    except Exception as error:
        print(error)
        return jsonify(error = str(error)), 400
    

@app.route("/stats/season/<season_id>")
def season_stats(season_id):
    print(season_id)
    try:
        stats = get_season_stats(season_id)
        return jsonify(stats)
    except Exception as error:
        print(error)
        return jsonify(error = str(error)), 400
    

@app.route("/stats/discipline/<discipline>")
def discipline_stats(discipline):
    print(discipline)
    try:
        stats = get_discipline_stats(discipline)
        return jsonify(stats)
    except Exception as error:
        print(error)
        return jsonify(error = str(error)), 400
    

@app.route("/stats/competitor/<competitor_id>")
def competitor_stats(competitor_id):
    print(competitor_id)
    try:
        stats = get_competitor_stats(competitor_id)
        return jsonify(stats)
    except Exception as error:
        print(error)
        return jsonify(error = str(error)), 400
    

@app.route("/stats/tournaments/<tournament_id>")
def tournament_stats(tournament_id):
    print(tournament_id)
    try:
        stats = get_tournament_stats(tournament_id)
        return jsonify(stats)
    except Exception as error:
        print(error)
        return jsonify(error = str(error)), 400