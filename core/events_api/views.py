from flask import (
    request, redirect, url_for, current_app
)
from . import event
from core.extensions import (
    bcrypt, cors
)
from core.auth.views import login_required
import datetime as d
from .helpers import date_serializer
from json import dumps

# def event_permission(f):
#     @wraps(f)
#     def function(*args, **kwargs):
#         if args[0]['is_moderator']:
#             return f(*args, **kwargs)
#         return {

#         }
schema = "platform_db"


@event.route("/", methods=['POST'])
@login_required
def add_event(current_user):
    if current_user['is_moderator']:
        db = current_app.config['DB']
        data = request.get_json(force=True)
        try:
            new_event = db.insert(
                "platform_db", "Event",
                [
                    {
                        "event_name": data['event_name'],
                        "duration": data['duration'],
                        "thumbnail": data['thumbnail'],
                        "description": data['description'],
                        "start_time": data['start_time'],
                        "end_time": data['end_time'],
                        "user_hash": current_user['user_id'],
                        "interaction_stats": [],
                        "date_created": dumps(
                            d.datetime.utcnow(),
                            default=date_serializer
                        )
                    }
                ]
            )
            # create event's reactions instance
            print(new_event)
            event_reactions = db.insert(
                schema, "reaction", [
                    {
                        "like": 0,
                        "event_id": new_event['inserted_hashes'][0],
                        "dislike": 0
                    }
                ]
            )
            return {
                "status":"ok",
                "message":"created event successfully"
            }, 200
        except Exception as e:
            raise e
            return {
                "status":"Error",
                "message":"An error occurred while trying to create the event."
            }, 503
    else:
        return {
            "status": "Error",
            "message": "User doesn't have permission to perform action"
        }, 401


@event.route("<event_id>/like", methods=['PUT'])
@login_required
def like(current_user, event_id):
    db = current_app.config['DB']
    # find event's like instance
    event_likes = db.search_by_value(
        schema, "reaction", "event_id",event_id, get_attributes=['*']
    )
    if len(event_likes) >= 1:
        try:
            db.update(
                schema, "reaction", [
                    {
                        "reaction_id": event_likes[0]['reaction_id'],
                        "event_id": event_id,
                        "like": event_likes[0]['like'] + 1
                    }
                ]
            )
            return {
                "status": "ok",
                "message": "Liked event successfully"
            }
        except Exception as e:
            raise e
            return {
                "status": "Error",
                "message": "Unable to add like, an error occurred."
            }, 503