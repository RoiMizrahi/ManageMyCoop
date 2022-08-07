import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)

app.config['SECRET_KEY']= 'mysecret'

#######################
####DATABASE SETUP#####
#######################

basedir = os.path.abspath(os.path.dirname(__file__))
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['DATABASE_URL'] = 'postgres://xtwcexeekdmmad:b140e5d694ff29d05d5abd747ccd07131d7811f58de83bc99da421c44db5c65b@ec2-50-19-255-190.compute-1.amazonaws.com:5432/d27n0gudtedosa'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

##########################
###LOGIN CONFIGURATION####
##########################

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'users.login'



from application.core.views import core
from application.users.views import users
from application.error_pages.handlers import error_pages
from application.egg_posts.views import egg_posts
from application.model.views import model

app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(error_pages)
app.register_blueprint(egg_posts)
app.register_blueprint(model)
