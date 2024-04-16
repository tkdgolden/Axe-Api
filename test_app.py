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
                                     "competitor_id": 6})
            resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)

            resp = client.put('/competitors',
                               json={"first_name": "david", "last_name": "duffey",
                                     "competitor_id": 6})
            json = resp.get_data(as_text=True)
            self.assertIn("A competitor with this name already exists.", json)

            resp = client.put('/competitors',
                               json={"first_name": "david", "last_name": "duffey"})
            json = resp.get_data(as_text=True)
            self.assertIn("A competitor requires an id to edit.", json)


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