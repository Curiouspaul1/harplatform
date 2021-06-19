from core import create_app
import os

app = create_app("default" or os.getenv('APP_CONFIG'))
db = app.config['DB']

@app.shell_context_processor
def make_shell_context(): 
    return dict(app=app, db=db)

