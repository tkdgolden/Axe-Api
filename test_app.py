import datetime
from unittest import TestCase
from app import app
from db import *


CUR, conn = db_connect()

class JudgeRouteTestCase(TestCase):
    """ tests judge routes """

    def test_verify_judge(self):
        """ tests judge verification """

        with app.test_client() as client:
            resp = client.post('/judges/verify',
                               json={"name": "judge1", "password": "pAsSwOrD"})
            resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)

            resp = client.post('/judges/verify',
                               json={"name": "judge1", "password": "wrong"})
            json = resp.get_data(as_text=True)
            self.assertIn("The password didn\'t match.", json)

            resp = client.post('/judges/verify',
                               json={"name": "judge14", "password": "wrong"})
            json = resp.get_data(as_text=True)
            self.assertIn("The judge name was not found.", json)

            resp = client.post('/judges/verify',
                               json={"password": "wrong"})
            json = resp.get_data(as_text=True)
            self.assertIn("A judge requires a name and password.", json)


    def test_add_judge(self):
        """ tests a new judge can be added """

        with app.test_client() as client:

            resp = client.post('/judges/new', 
                               json={"name": "judge2", "password": "1234"})
            json = resp.get_data(as_text=True)
            self.assertIn("You must be logged in for this action.", json)
            
            with client.session_transaction() as change_session:
                change_session["user_id"] = 1

            resp = client.post('/judges/new', 
                               json={"name": "judge2", "password": "1234"})
            resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 201)

            resp = client.post('/judges/new', 
                               json={"name": "judge2", "password": "1234"})
            json = resp.get_data(as_text=True)
            self.assertIn("A judge with this name already exists.", json)

            resp = client.post('/judges/new', 
                               json={"name": "judge2"})
            json = resp.get_data(as_text=True)
            self.assertIn("A new judge requires a name and password.", json)

        CUR.execute(""" SELECT * FROM judges """)
        all_judges = str(CUR.fetchall())
        
        self.assertIn("judge2", all_judges)


class CompetitorRouteTestCase(TestCase):
    """ tests competitor routes """

    def test_add_competitor(self):
        """ tests adding a new competitor """

        with app.test_client() as client:

            resp = client.post('/competitors',
                               json={"first_name": "david", "last_name": "duffey"})
            json = resp.get_data(as_text=True)
            self.assertIn("You must be logged in for this action.", json)

            with client.session_transaction() as change_session:
                change_session["user_id"] = 1

            resp = client.post('/competitors',
                               json={"first_name": "david", "last_name": "duffey"})
            resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 201)

            resp = client.post('/competitors',
                               json={"first_name": "david"})
            json = resp.get_data(as_text=True)
            self.assertIn("A new competitor requires a first and last name.", json)

            resp = client.post('/competitors',
                               json={"first_name": "david", "last_name": "duffey"})
            json = resp.get_data(as_text=True)
            self.assertIn("A competitor with this name already exists.", json)

        CUR.execute(""" SELECT * FROM competitors """)
        all_competitors = CUR.fetchall()
        
        self.assertIn([4, 'david', 'duffey'], all_competitors)

    def test_edit_competitor(self):
        """ tests editing a competitor """

        with app.test_client() as client:

            resp = client.put('/competitors',
                               json={"first_name": "david",
                                     "last_name": "duffy",
                                     "competitor_id": 6})
            json = resp.get_data(as_text=True)
            self.assertIn("You must be logged in for this action.", json)

            with client.session_transaction() as change_session:
                change_session["user_id"] = 1

            resp = client.put('/competitors',
                               json={"first_name": "david",
                                     "last_name": "duffy",
                                     "competitor_id": 4})
            resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)

            resp = client.put('/competitors',
                               json={"first_name": "david", "last_name": "duffy",
                                     "competitor_id": 4})
            json = resp.get_data(as_text=True)
            self.assertIn("A competitor with this name already exists.", json)

            resp = client.put('/competitors',
                               json={"first_name": "david", "last_name": "duffey"})
            json = resp.get_data(as_text=True)
            self.assertIn("A competitor requires an id to edit.", json)
            
        CUR.execute(""" SELECT * FROM competitors """)
        all_competitors = CUR.fetchall()
        
        self.assertIn([4, 'david', 'duffy'], all_competitors)


class SeasonRouteTestCase(TestCase):
    """ tests season routes """

    def test_add_season(self):
        """ tests adding a new season """

        with app.test_client() as client:

            resp = client.post('/seasons')
            json = resp.get_data(as_text=True)
            self.assertIn("You must be logged in for this action.", json)

            with client.session_transaction() as change_session:
                change_session["user_id"] = 1

            resp = client.post('/seasons',
                               json={"season": "I", "start_date": "2022-02-22"})
            resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 201)

            resp = client.post('/seasons',
                               json={"season": "I"})
            json = resp.get_data(as_text=True)
            self.assertIn("A new season requires a season and start date.", json)

            resp = client.post('/seasons',
                               json={"season": "I", "start_date": "2024-08-15"})
            json = resp.get_data(as_text=True)
            self.assertIn("A similar season already exists for the given year.", json)

        CUR.execute(""" SELECT * FROM seasons """)
        all_seasons = CUR.fetchall()

        self.assertIn([3, 'I', datetime.date(2022, 2, 22)], all_seasons)


class QuarterRouteTestCase(TestCase):
    """ tests quarter routes """

    def test_add_quarter(self):
        """ tests adding a new quarter """

        with app.test_client() as client:

            resp = client.post('/quarters')
            json = resp.get_data(as_text=True)
            self.assertIn("You must be logged in for this action.", json)

            with client.session_transaction() as change_session:
                change_session["user_id"] = 1

            resp = client.post('/quarters',
                               json={"month": 1, "season_id": 2, "start_date": "2022-02-22"})
            resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 201)

            resp = client.post('/quarters',
                               json={"month": 1})
            json = resp.get_data(as_text=True)
            self.assertIn("A new quarter requires a month, season id, and start date.", json)

            resp = client.post('/quarters',
                               json={"month": 1, "start_date": "2022-08-15", "season_id": 2})
            json = resp.get_data(as_text=True)
            self.assertIn("A similar quarter already exists for the given season.", json)

        CUR.execute(""" SELECT * FROM quarters """)
        all_quarters = CUR.fetchall()

        self.assertIn([3, 2, 1, datetime.date(2022, 2, 22)], all_quarters)


class LapRouteTestCase(TestCase):
    """ tests lap routes """

    def test_add_lap(self):
        """ tests adding a new lap """

        with app.test_client() as client:

            resp = client.post('/laps')
            json = resp.get_data(as_text=True)
            self.assertIn("You must be logged in for this action.", json)

            with client.session_transaction() as change_session:
                change_session["user_id"] = 1

            resp = client.post('/laps',
                               json={"lap": 3, "quarter_id": 2, "discipline": "knives", "start_date": "2022-08-20"})
            resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 201)

            resp = client.post('/laps',
                               json={"lap": 3, "quarter_id": 2, "start_date": "2022-08-15"})
            json = resp.get_data(as_text=True)
            self.assertIn("A new lap requires a lap, quarter id, discipline, and start date.", json)

            resp = client.post('/laps',
                               json={"lap": 3, "quarter_id": 2, "discipline": "knives", "start_date": "2022-08-20"})
            json = resp.get_data(as_text=True)
            self.assertIn("A similar lap already exists for the given quarter.", json)

        CUR.execute(""" SELECT * FROM laps """)
        all_laps = CUR.fetchall()

        self.assertIn([3, 2, 3, 'knives', datetime.date(2022, 8, 20)], all_laps)


class EnrollmentRouteTestCase(TestCase):
    """ tests enrollment routes """

    def test_add_enrollment(self):
        """ tests adding a new enrollment """

        CUR.execute(""" SELECT * FROM enrollment """)
        all_enrollment = CUR.fetchall()

        with app.test_client() as client:

            resp = client.post('/enrollment')
            json = resp.get_data(as_text=True)
            self.assertIn("You must be logged in for this action.", json)

            with client.session_transaction() as change_session:
                change_session["user_id"] = 1

            resp = client.post('/enrollment',
                               json={"competitor_id": 2, "season_id": 2})
            resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 201)
            
            resp = client.post('/enrollment',
                               json={"competitor_id": 3, "tournament_id": 1})
            resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 201)

            resp = client.post('/enrollment',
                               json={"competitor_id": 2})
            json = resp.get_data(as_text=True)
            self.assertIn("Enrollment requires a competitor id and either a season id or a tournament id.", json)

            resp = client.post('/enrollment',
                               json={"season_id": 2, "tournament_id": 1})
            json = resp.get_data(as_text=True)
            self.assertIn("Enrollment requires a competitor id and either a season id or a tournament id.", json)

            resp = client.post('/enrollment',
                               json={"competitor_id": 2, "season_id": 2})
            json = resp.get_data(as_text=True)
            self.assertIn("This competitor is already enrolled.", json)

        CUR.execute(""" SELECT * FROM enrollment """)
        all_enrollment = CUR.fetchall()

        self.assertIn([2, None, 2], all_enrollment)
        self.assertIn([None, 1, 3], all_enrollment)