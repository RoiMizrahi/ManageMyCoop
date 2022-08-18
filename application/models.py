from application import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer , primary_key = True)
    profile_image = db.Column(db.String(64), nullable= False, default = 'default_profile.png')
    email = db.Column(db.String(64), unique =True, index = True)
    username = db.Column(db.String(64), unique= True, index = True)
    first_name = db.Column(db.String(64), nullable= False)
    last_name = db.Column(db.String(64), nullable= False)
    phone = db.Column(db.String(64), nullable= False)
    password_hash = db.Column(db.String(128))

    posts = db.relationship('EggPost', backref='collector', lazy = True)

    def __init__(self,email,username, first_name,last_name,phone,password):
        self.email = email
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.password_hash = generate_password_hash(password)

    def check_password(self , password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"Username is {self.username} User Full name {self.last_name} {self.first_name}"

class EggPost(db.Model):

    users = db.relationship(User)

    id = db.Column(db.Integer , primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    date = db.Column(db.DateTime,nullable=False, default=datetime.utcnow)
    eggs_amount = db.Column(db.Integer)
    broken_eggs = db.Column(db.Integer)
    current_food = db.Column(db.Integer)
    dead_chicken = db.Column(db.Integer, nullable= True)

    def __init__(self, user_id ,eggs_amount,broken_eggs,current_food,dead_chicken):
        self.user_id = user_id
        self.eggs_amount = eggs_amount
        self.broken_eggs = broken_eggs
        self.current_food = current_food
        self.dead_chicken = dead_chicken

    def __repr__(self):
        return f"Collected eggs at {self.date}, by {self.user_id.username}"
