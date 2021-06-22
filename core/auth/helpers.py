from functools import wraps
from flask import request
import jwt
from jwt.exceptions import InvalidSignatureError

def login_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        app = kwargs['app']
        db = app.config['DB']
        key = app.config['SECRET']
        if "access_token" in request.cookies:
            token = request.cookies.get('access_token')
            if token:
                uid = jwt.decode(token, key)
                current_user = db.search_by_hash(
                    "platform_db", "User",
                    [uid], get_attributes=["*"]
                )[0]
                return f(current_user, *args, **kwargs)
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