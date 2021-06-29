from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_socketio import SocketIO
# initialize app dependencies
bcrypt = Bcrypt()
cors = CORS()
socket = SocketIO()
