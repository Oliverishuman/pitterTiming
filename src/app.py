import os
import sys
from flask import Flask
from flask_login import LoginManager


# Add src directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from user import User
from db import init_db
from routes import routes

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev_secret_key')

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'routes.login'

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Register Blueprint
app.register_blueprint(routes)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)