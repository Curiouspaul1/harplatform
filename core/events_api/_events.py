from os import name
from core.extensions import socket
from flask_socketio import emit, join_room, leave_room
from flask import current_app
import json

schema = "platform_db"


@socket.on('joined')
def joined(data):
    room = data['event_name']
    join_room(room)


@socket.on('send_comment')
def leave_comment(data):
    data = json.loads(data)
    db = current_app.config['DB']
    room = data['event_name']
    # create comment 
    db.insert(
        schema, "Comment", [
            {
                "body": data['comment_body'],
                "file_url": data['file_url'],
                "sender_name": data['sender_name'],
                "event_id": data['event_id']
            }
        ]
    )
    # broadcast comment
    emit(
        'message',
        {'data': data['sender_name']+": " + data['comment_body']},
        room=room
    )


@socket.on('left')
def leave_room(data):
    room = data['event_name']
    leave_room(room)
