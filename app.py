from datetime import datetime
from flask import Flask, jsonify, request, session, json
from db import *
from auth import login_required
from judge import *
from competitor import *
from season import *
from quarter import *
from lap import *
from enrollment import *
import os


app = Flask(__name__)
app.secret_key = os.urandom(12).hex()

db_connect()


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
        session["user_id"] = judge_id
        return jsonify(success = True)
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