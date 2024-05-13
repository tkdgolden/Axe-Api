from db import db_connect

CUR, conn = db_connect()

def get_overall_stats():
    """ all player stats selects from all scores """

    try:
        CUR.execute(""" SELECT competitor_id, competitor_first_name || ' ' || competitor_last_name full_name, ROUND(AVG(total), 2), COUNT(win), COUNT(score_id), MAX(total), MIN(total) FROM scores JOIN competitors USING (competitor_id) GROUP BY competitor_id, full_name ORDER BY full_name """)
        all_stats = CUR.fetchall()

    except:
        conn.rollback()
        raise

    return all_stats