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
        
        self.assertIn([4, 'fname test', 'lname test'], all_competitors)

    def test_no_duplicate_competitor(self):
        """ failure to add competitor because already exists """

        with self.assertRaises(ValueError):
            add_competitor("ann", "applewood")

        add_competitor("ann", "applesmith")

        CUR.execute(""" SELECT * FROM competitors """)
        all_competitors = CUR.fetchall()
        
        self.assertIn([5, 'ann', 'applesmith'], all_competitors)

    def test_edit_competitor(self):
        """ tests an existing competitor gets changed """

        edit_competitor(3, "fname test edit", "lname test edit")

        CUR.execute(""" SELECT * FROM competitors """)
        all_competitors = CUR.fetchall()
        
        self.assertIn([3, 'fname test edit', 'lname test edit'], all_competitors)

    def test_edit_no_duplicate_competitor(self):
        """ failure to edit competitor because already exists """

        with self.assertRaises(ValueError):
            edit_competitor(5, "ann", "applewood")

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

    def test_add_season_enrollment(self):
        """ tests adding a new enrollment to a season """

        with self.assertRaises(Exception):
            add_enrollment(season_id=1, competitor_id=6)

        add_enrollment(season_id=1, competitor_id=2)

        CUR.execute(""" SELECT * FROM enrollment """)
        all_enrollment = CUR.fetchall()

        self.assertIn([None, 1, 2], all_enrollment)

    def test_add_tournament_enrollment(self):
        """ tests adding a new enrollment to a tournament """

        with self.assertRaises(Exception):
            add_enrollment(tournament_id=1, competitor_id=6)

        add_enrollment(tournament_id=1, competitor_id=2)

        CUR.execute(""" SELECT * FROM enrollment """)
        all_enrollment = CUR.fetchall()

        self.assertIn([1, None, 2], all_enrollment)

class TournamentTestCase(TestCase):
    """ testing methods involving tournaments table """

    def test_no_duplicate_tournament(self):
        """ tests duplicate tournament checker """

        self.assertFalse(no_duplicate_tournament('Hatchet Fight', 'hatchet', '2024-01-20'))
        self.assertTrue(no_duplicate_tournament('Knife Fight', 'Knives', '2024-01-20'))

    def test_add_tournament(self):
        """ tests adding a new tournament """

        add_tournament('Fight Test', 'Knives', '2024-12-22')

        CUR.execute(""" SELECT * FROM tournaments """)
        all_tournaments = CUR.fetchall()

        self.assertIn([3, 'Fight Test', 'Knives', datetime.date(2024, 12, 22), True, None, False], all_tournaments)

    def test_update_tournament_enrollment(self):
        """ tests update tournament enrollment """

        update_tournament_enrollment(1)

        CUR.execute(""" SELECT * FROM tournaments WHERE tournament_id = 1 """)
        tournament = CUR.fetchone()

        self.assertFalse(tournament["enrollment_open"])

    def test_update_tournament_current_round(self):
        """ tests update tournament current round """

        update_tournament_current_round(2, 1)

        CUR.execute(""" SELECT * FROM tournaments WHERE tournament_id = 2 """)
        tournament = CUR.fetchone()

        self.assertEqual(1, tournament["current_round"])

class RoundTestCase(TestCase):
    """ testing methods involving rounds table """

    def test_add_round(self):
        """ tests adding a new round """

        add_round(1, '{0, 0}', '{105, 106}', 'B')

        CUR.execute(""" SELECT * FROM rounds """)
        all_rounds = CUR.fetchall()

        self.assertIn([3, [105, 106], [0, 0], 1, 'B'], all_rounds)

class MatchTestCase(TestCase):
    """ testing methods involving matches table """

    def test_add_unscored_tournament_match(self):
        """ tests adding a new empty match in a tournament """

        add_unscored_tournament_match(2, 3, 1)

        CUR.execute(""" SELECT * FROM matches WHERE player_1_id = 2 AND player_2_id = 3 """)
        all_matches = CUR.fetchall()

        self.assertIn([4, 2, 3, None, 1, None, None, None, None, None, None], all_matches)

    def test_add_unscored_season_match(self):
        """ tests adding a new empty match in a season """

        add_unscored_season_match(2, 3, 1)

        CUR.execute(""" SELECT * FROM matches WHERE match_id = 3 """)
        all_matches = CUR.fetchall()

        self.assertIn([3, 2, 3, None, None, 1, None, None, None, None, None], all_matches)

    def test_update_completed_match(self):
        """ tests updating a match with complete data """

        update_completed_match(1, 1, "hatchet", 1, '2024-01-08 04:05:06', 12, 35)

        CUR.execute(""" SELECT * FROM matches WHERE match_id = 1 """)
        all_matches = CUR.fetchall()

        self.assertIn([1, 1, 2, 1, 1, None, 'hatchet', 1, datetime.datetime(2024, 1, 8, 4, 5, 6), 12, 35], all_matches)