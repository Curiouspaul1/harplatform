from core import create_app, socket
import os

app = create_app("default" or os.getenv('APP_CONFIG'))
db = app.config['DB']

@app.shell_context_processor
def make_shell_context(): 
    return dict(app=app, db=db)

if __name__ == "__main__":
    socket.run(app)
