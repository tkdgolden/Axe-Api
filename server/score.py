from db import db_connect

CUR, conn = db_connect()


def add_player_score(competitor_id, match_id, quick_points, sequence, throw1, throw2, throw3, throw4, throw5, throw6, throw7, throw8, total, win):
    """ adds a players score data from a match """

    try:
        CUR.execute(""" INSERT INTO scores (competitor_id, match_id, quick_points, sequence, throw1, throw2, throw3, throw4, throw5, throw6, throw7, throw8, total, win) VALUES (%(competitor_id)s, %(match_id)s, %(quick_points)s, %(sequence)s, %(throw1)s, %(throw2)s, %(throw3)s, %(throw4)s, %(throw5)s, %(throw6)s, %(throw7)s, %(throw8)s, %(total)s, %(win)s) """,
                    {'competitor_id': competitor_id,
                     'match_id': match_id,
                     'quick_points': quick_points,
                     'sequence': sequence,
                     'throw1': throw1,
                     'throw2': throw2,
                     'throw3': throw3,
                     'throw4': throw4,
                     'throw5': throw5,
                     'throw6': throw6,
                     'throw7': throw7,
                     'throw8': throw8,
                     'total': total,
                     'win': win})
        conn.commit()

    except:
        conn.rollback()
        raise