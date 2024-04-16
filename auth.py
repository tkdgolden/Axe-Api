from functools import wraps
from flask import session, jsonify


def login_required(f):
    """ checks that a judge is logged in """

    @wraps(f)
    def check_login(*args, **kwargs):
        if session.get("user_id") is None:
            error = "You must be logged in for this action."
            print(error)
            return jsonify(error), 401
        return (f(*args, **kwargs))
    return check_login