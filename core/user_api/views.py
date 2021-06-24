from flask import (
    current_app, request
)
from core.extensions import (
    bcrypt, cors
)
# from harperdb.exceptions import HarperDBError
from . import user
from core.auth.views import login_required

schema = "platform_db"

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
    # check to see if email already exists
    user = db.search_by_value(
        schema, "User", "email",
        data['email'], get_attributes=['*']
    )
    # print(user)
    if user == []:
        try:
            new_user = db.insert(
                schema, "User",
                [ 
                    {
                        "name": data['name'],
                        "username": data['username'],
                        "email":data['email'], 
                        "password":pw_hash,
                        "profile_photo":data['profile_photo'],
                        "profile_photo_id":data['profile_photo_id'],
                        "is_moderator":data['is_moderator'],
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
    else:
        return {
            "status": "Error",
            "message": "User with email already exists"
        }, 401
