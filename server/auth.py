from functools import wraps
import os
from flask import request, session, jsonify
import jwt
from judge import *

SECRET_KEY = os.urandom(12).hex()

def login_required(f):
    """ checks that a judge is logged in """

    # @wraps(f)
    # def check_login(*args, **kwargs):
    #     print(session.get("user_id"))
    #     if session.get("user_id") is None:
    #         error = "You must be logged in for this action."
    #         print(error)
    #         return jsonify(error), 401
    #     return (f(*args, **kwargs))
    # return check_login

    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        # ensure the jwt-token is passed with the headers
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        if not token: # throw error if no token provided
            return jsonify({"error": "A valid token is missing!"}), 401
        try:
           # decode the token to obtain user public_id
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], options={'verify_signature': False})
            current_user = get_judge(data['user_id'])
        except:
            return jsonify({"error": "Invalid token!"}), 401
         # Return the user information attached to the token
        return f(*args, **kwargs)
    return decorator