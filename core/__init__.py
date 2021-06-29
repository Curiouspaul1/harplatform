from flask import Flask
from config import config
from .extensions import (
    bcrypt, cors, socket
)

def create_app(config_name):
    # instantiate flask app instance
    app = Flask(__name__)

    # add config
    app.config.from_object(config[config_name])

    # add app instance to dependenciess
    bcrypt.init_app(app)
    cors.init_app(app)
    socket.init_app(app, cors_allowed_origins='*')
    
    # register blueprints
    from .events_api import event
    from .user_api import user
    from .auth import auth
 
    app.register_blueprint(event, url_prefix="/event")
    app.register_blueprint(user, url_prefix="/user")
    app.register_blueprint(auth, url_prefix="/auth")

    return app
