# from the terminal run:
# psql < test_seed.sql
# python3 -m unittest

from db import *
from unittest import TestCase
import datetime


CUR = db_connect()

class JudgeTestCase(TestCase):
    """ testing methods involving judge table """
        
    def test_add_judge(self):
        """ tests a new judge gets added to db """

        add_judge("test name", "tEsTpAsS")

        CUR.execute(""" SELECT * FROM judges """)
        all_judges = str(CUR.fetchall())
        
        self.assertIn("test name", all_judges)
        self.assertNotIn("tEsTpAsS", all_judges)

    def test_no_duplicate_judge(self):
        """ failure to add judge because already exists """

        with self.assertRaises(ValueError):
            add_judge("judge1", "tEsTpAsS")

    def test_verify_judge(self):
        """ tests judge verification method """

        judge = verify_judge("judge1", "pAsSwOrD")

        self.assertIn('judge1', judge)

        with self.assertRaises(ValueError):
            verify_judge("judge1", "tEsTpAsS")

        with self.assertRaises(ValueError):
            verify_judge("judge2", "pAsSwOrD")

class CompetitorTestCase(TestCase):
    """ testing methods involving competitor table """
        
    def test_add_competitor(self):
        """ tests a new competitor gets added to db """

        add_competitor("fname test", "lname test")

        CUR.execute(""" SELECT * FROM competitors """)
        all_competitors = CUR.fetchall()
        
        self.assertIn([3, 'fname test', 'lname test'], all_competitors)

    def test_no_duplicate_competitor(self):
        """ failure to add competitor because already exists """

        with self.assertRaises(ValueError):
            add_competitor("ann", "applewood")

        add_competitor("ann", "applesmith")

        CUR.execute(""" SELECT * FROM competitors """)
        all_competitors = CUR.fetchall()
        
        self.assertIn([4, 'ann', 'applesmith'], all_competitors)

    def test_edit_competitor(self):
        """ tests an existing competitor gets changed """

        edit_competitor(2, "fname test edit", "lname test edit")

        CUR.execute(""" SELECT * FROM competitors """)
        all_competitors = CUR.fetchall()
        
        self.assertIn([2, 'fname test edit', 'lname test edit'], all_competitors)

    def test_edit_no_duplicate_competitor(self):
        """ failure to edit competitor because already exists """

        with self.assertRaises(ValueError):
            edit_competitor(4, "ann", "applewood")

class SeasonTestCase(TestCase):
    """ testing methods involving seasons table """

    def test_no_duplicate_season(self):
        """ tests duplicate season checker """

        self.assertFalse(no_duplicate_season('I', datetime.date(2024, 2, 12)))
        self.assertTrue(no_duplicate_season('I', datetime.date(2023, 2, 12)))

    def test_add_season(self):
        """ tests adding a new season """

        add_season('III', datetime.date(2023, 2, 12))

        CUR.execute(""" SELECT * FROM seasons """)
        all_seasons = CUR.fetchall()

        self.assertIn([3, 'III', datetime.date(2023, 2, 12)], all_seasons)

class QuarterTestCase(TestCase):
    """ testing methods involving quarters table """

    def test_no_duplicate_quarter(self):
        """ tests duplicate quarter checker """

        self.assertFalse(no_duplicate_quarter(1, 1))
        self.assertTrue(no_duplicate_quarter(2, 2))

    def test_add_quarter(self):
        """ tests adding a new quarter """

        with self.assertRaises(Exception):
            add_quarter(1, 3, '2024-01-20')

        add_quarter(6, 1, '2024-12-12')

        CUR.execute(""" SELECT * FROM quarters """)
        all_quarters = CUR.fetchall()

        self.assertIn([4, 1, 6, datetime.date(2024, 12, 12)], all_quarters)

class LapTestCase(TestCase):
    """ testing methods involving laps table """

    def test_no_duplicate_lap(self):
        """ tests duplicate lap checker """

        self.assertFalse(no_duplicate_lap(1, 1, 'hatchet'))
        self.assertTrue(no_duplicate_lap(1, 1, 'knives'))

    def test_add_lap(self):
        """ tests adding a new lap """

        with self.assertRaises(Exception):
            add_lap(10, 1, 'hatchet', '2024-08-15')

        add_lap(2, 2, 'hatchet', '2024-08-15')

        CUR.execute(""" SELECT * FROM laps """)
        all_laps = CUR.fetchall()

        self.assertIn([4, 2, 2, 'hatchet', datetime.date(2024, 8, 15)], all_laps)

class EnrollmentTestCase(TestCase):
    """ testing methods involving enrollment table """

    def test_no_duplicate_enrollment(self):
        """ tests duplicate enrollment checker """

        self.assertFalse(no_duplicate_enrollment(season_id=1, competitor_id=1))
        self.assertTrue(no_duplicate_enrollment(season_id=2, competitor_id=1))

    def test_add_enrollment(self):
        """ tests adding a new enrollment """

        with self.assertRaises(Exception):
            add_enrollment(season_id=1, competitor_id=6)

        add_enrollment(season_id=1, competitor_id=2)

        CUR.execute(""" SELECT * FROM enrollment """)
        all_enrollment = CUR.fetchall()

        self.assertIn([None, 1, 2], all_enrollment)