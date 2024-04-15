from db import db_connect
from werkzeug.security import generate_password_hash, check_password_hash


CUR, conn = db_connect()

def add_judge(name, password):
    """ hash password, create new judge """

    try:
        pwhash = generate_password_hash(password)

        CUR.execute(""" INSERT INTO judges(judge_name, pass_hash) VALUES (%(name)s, %(pwhash)s) """,
                    {'name': name, 'pwhash': pwhash})

        conn.commit()

    except:
        conn.rollback()
        raise ValueError("A judge with this name already exists.")
    

def verify_judge(name, password):
    """ verify's judge name and hashed password match """

    try:
        CUR.execute(""" SELECT * FROM judges WHERE judge_name = %(name)s """, 
                    {'name': name})
        all_judges = CUR.fetchall()

    except:
        conn.rollback()
        raise

    if len(all_judges) != 1:
        raise ValueError("The judge name was not found.")
    
    pass_hash = all_judges[0]["pass_hash"]
    
    if not check_password_hash(pass_hash, password):
        raise ValueError("The password didn't match.")
    else:
        # a more efficient, readable way to unpack this? vvv
        return all_judges[0]["judge_id"], all_judges[0]["judge_name"]