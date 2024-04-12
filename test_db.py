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