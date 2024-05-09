from datetime import datetime
from flask import Flask, jsonify, request, session, json
import jwt
from db import *
from auth import login_required, SECRET_KEY
from judge import *
from competitor import *
from season import *
from quarter import *
from lap import *
from enrollment import *
from tournament import *
from round import *
from match import *
from score import *
import os
from flask_cors import CORS

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
            add_competitor(first_name, last_name)
            return jsonify(success=True), 201
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
    

@app.route('/quarters', methods=["POST"])
@login_required
def quarter():
    """ create a new quarter """

    try:
        month = request.json["month"]
        season_id = request.json["season_id"]
        start_date = datetime.strptime(request.json["start_date"], '%Y-%m-%d')
    except:
        error = "A new quarter requires a month, season id, and start date."
        print(error)
        return jsonify(error), 400
    
    try:
        add_quarter(month, season_id, start_date)
        return jsonify(success=True), 201
    except Exception as error:
        print(error)
        return jsonify(error = str(error)), 400
    

@app.route('/laps', methods=["POST"])
@login_required
def lap():
    """ create a new lap """

    try:
        counter = request.json["lap"]
        quarter_id = request.json["quarter_id"]
        discipline = request.json["discipline"]
        start_date = datetime.strptime(request.json["start_date"], '%Y-%m-%d')
    except:
        error = "A new lap requires a lap, quarter id, discipline, and start date."
        print(error)
        return jsonify(error), 400
    
    try:
        add_lap(quarter_id, counter, discipline, start_date)
        return jsonify(success=True), 201
    except Exception as error:
        print(error)
        return jsonify(error = str(error)), 400
    

@app.route('/enrollment', methods=["POST"])
@login_required
def enrollment():
    """ enrolls a competitor to a season or tournament """

    try:
        competitor_id = request.json["competitor_id"]
        if ("season_id" in request.json and "tournament_id" in request.json):
            raise
        elif ("season_id" in request.json):
            season_id = request.json["season_id"]
            tournament_id = None
        elif ("tournament_id" in request.json):
            tournament_id = request.json["tournament_id"]
            season_id = None
        else:
            raise
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