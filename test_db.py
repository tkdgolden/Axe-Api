# from the terminal run:
# psql < test_seed.sql
# python3 -m unittest

from db import *
from unittest import TestCase


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

class CompetitorTestCase(TestCase):
    """ testing methods involving competitor table """
        
    def test_add_competitor(self):
        """ tests a new competitor gets added to db """

        add_competitor("fname test", "lname test")

        CUR.execute(""" SELECT * FROM competitors """)
        all_competitors = str(CUR.fetchall())
        
        self.assertIn("fname", all_competitors)

    def test_no_duplicate_competitor(self):
        """ failure to add competitor because already exists """

        with self.assertRaises(ValueError):
            add_competitor("ann", "applewood")

        add_competitor("ann", "applesmith")

        CUR.execute(""" SELECT * FROM competitors """)
        all_competitors = str(CUR.fetchall())
        
        self.assertIn("applesmith", all_competitors)

    def test_edit_competitor(self):
        """ tests an existing competitor gets changed """

        edit_competitor(2, "fname test edit", "lname test edit")

        CUR.execute(""" SELECT * FROM competitors """)
        all_competitors = str(CUR.fetchall())
        
        self.assertIn("edit", all_competitors)

    def test_edit_no_duplicate_competitor(self):
        """ failure to edit competitor because already exists """

        with self.assertRaises(ValueError):
            edit_competitor(4, "ann", "applewood")