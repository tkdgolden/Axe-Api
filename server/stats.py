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


def get_season_stats(season_id):
    try:
        CUR.execute(""" SELECT competitors.competitor_id, competitor_first_name || ' ' || competitor_last_name full_name, ROUND(AVG(total), 2), COUNT(win), COUNT(score_id), MAX(total), MIN(total) FROM scores JOIN matches ON scores.match_id = matches.match_id JOIN laps ON matches.lap_id = laps.lap_id JOIN quarters ON laps.quarter_id = quarters.quarter_id JOIN seasons ON quarters.season_id = seasons.season_id JOIN competitors ON scores.competitor_id = competitors.competitor_id WHERE seasons.season_id = %(season_id)s GROUP BY competitors.competitor_id, full_name ORDER BY full_name  """, {'season_id': season_id})
        season_stats = CUR.fetchall()
        print(season_stats)
    except:
        conn.rollback()
        raise
    return season_stats