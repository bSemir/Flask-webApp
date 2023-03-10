from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config["SECRET_KEY"] = "25fdd3c7d1e3e7462c36fdbeedbe66e7"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# tell the login_required decorator where is our login route located
login_manager.login_view = "login"
login_manager.login_message_category = "info"

from flaskblog import routes
