from flask import (
    current_app,  url_for, redirect, request,
    make_response
)
from core.extensions import (
    bcrypt, cors
)
from jwt.exceptions import *
import jwt
import datetime as d
from . import auth
from functools import wraps

schema = "platform_db"


def login_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        app = current_app
        db = app.config['DB']
        key = app.config['SECRET_KEY']
        if "access_token" in request.headers:
            token = request.headers['access_token']
            if token:
                try:
                    uid = jwt.decode(token, key, algorithms="HS256")
                    current_user = db.search_by_hash(
                        "platform_db", "User",
                        [uid['uid']], get_attributes=["*"]
                    )[0]
                    return f(current_user, *args, **kwargs)
                except ExpiredSignatureError:
                    return {
                        "status": "Error",
                        "message": "Expired token"
                    }, 401
                else:
                    return {
                        "status": "Error",
                        "message": "An error occurred while trying to decode token"
                    }
            else:
                return {
                    "status": "Error",
                    "message": "Token not set in headers"
                }, 401
        else:
            return {
                "status":  "Error",
                "message": "Token not in headers"
            }
    return function


@auth.route('/', methods=['POST'])
def login():
    db = current_app.config['DB']
    data = request.get_json(force=True)
    # TODO: Add functionality for username and email 
    # signup.
    # find user by email or username
    if "email" or "Email" in data.keys():
        user = db.search_by_value(
            "platform_db", "User",
            search_attribute="email",
            search_value=data['email'],
            get_attributes=['*']
        )[0]
        # if user is found compare hashses
        if bcrypt.check_password_hash(
            user['password'], data['password']
        ):
        # if hashes match generate tokens for the user
            access_token = jwt.encode(
                {
                    "uid":user['user_id'],
                    "exp":d.datetime.utcnow() + d.timedelta(minutes=60)
                },
                current_app.config['SECRET_KEY']
            )
            refresh_token = jwt.encode(
                {
                    "uid":user['user_id'],
                    "exp":d.datetime.utcnow() + d.timedelta(days=2)
                },
                current_app.config['SECRET_KEY']
            )
            return {
                "login":True,
                "access_token": access_token,
                "refresh_token": refresh_token
            }, 200
        else:
            return {
                "status": "error",
                "message": "Incorrect password"
            }, 401
    else:
        return {
            "status": "Error",
            "message": "Email field is empty"
        }, 401