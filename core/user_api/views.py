from flask import (
    current_app, request
)
from core.extensions import (
    bcrypt, cors
)
# from harperdb.exceptions import HarperDBError
from . import user
from core.auth.helpers import login_required


@user.route("/register", methods=['POST'])
def register():
    db = current_app.config['DB']
    data = request.get_json(force=True)
    # hash user password
    user_password = data['password']
    pw_hash = str(
        bcrypt.generate_password_hash(user_password),
        'utf-8'
    )
    try:
        new_user = db.insert(
            "platform_db", "User",
            [
                {
                    "name": data['name'],
                    "username": data['username'],
                    "email":data['email'],
                    "password":pw_hash,
                    "profile_photo":data['profile_photo'],
                    "profile_photo_id":data['profile_photo_id'],
                    "is_moderator":data['is_moderator']
                }
            ]
        )
        return {
            "status":"ok",
            "message":"User created succesfully"
        }, 200
    except Exception:
        return {
            "status":"error",
            "message":"An error occurred boss"
        }, 503


@user.route("/protected")
@login_required
def protect(current_user):
    return {
        "status": "Works"
    }, 200