from flask import Flask
from config import config
from harperdb import HarperDB
from flask_bcrypt import Bcrypt
from flask_cors import CORS


def create_app(config_name):
    # instantiate flask app instance
    app = Flask(__name__)

    # add config
    app.config.from_object(config[config_name])

    # initialize app dependencies
    bcrypt = Bcrypt(app)
    db = HarperDB(
        username=app.config['DATABASE_USERNAME'],
        password=app.config['DATABASE_PASSWORD'],
        url=app.config['DATABASE_URL']
    )
    cors = CORS(app)
    
    # register blueprints
    from .events_api import event
    from .user_api import user
    from .auth import auth
 
    app.register_blueprint(event, url_prefix="/event")
    app.register_blueprint(user, url_prefix="/user")
    app.register_blueprint(auth, url_prefix="/auth")

    return app

