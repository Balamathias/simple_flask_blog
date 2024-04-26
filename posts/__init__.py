'''
This file is used to initialize the package. 
It is used to import the routes module from the posts package. 
The routes module is used to define the routes for the application. 
The routes module is imported after the app and db objects are created. 
The app object is used to create the Flask application, and the db object is used to create the SQLAlchemy object. The SQLAlchemy object is used to interact with the database. The routes module is imported after the app and db objects are created because the routes module uses the app and db objects to define the routes for the application.
'''

from flask import Blueprint, Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'neGzyg773738HHUWUwgxebxddhdhwh&wubuiwekuwregcfbweuwehweh'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
marsh_mallow = Marshmallow(app)
api_view = Blueprint('api', __name__, url_prefix='/api/v1')

from posts import routes
from posts.api.v1 import api
