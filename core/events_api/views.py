from flask import (
    request, redirect, url_for, current_app
)
from . import event
from core.extensions import (
    bcrypt, cors
)

@event.route("/", methods=['POST'])
def add_article():
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
                    "interaction_stats": []
                }
            ]
        )
        return {
            "status":"ok",
            "message":"created event successfully"
        }, 200
    except Exception:
        return {
            "status":"Error",
            "message":"An error occurred while trying to create the event."
        }, 503
    