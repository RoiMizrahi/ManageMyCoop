from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms.validators import DataRequired

class EggPostForm(FlaskForm):
    eggs_amount = IntegerField("Number of eggs collected")
    broken_eggs = IntegerField("Number of broken eggs collected")
    current_food = IntegerField ("Amount of food")
    dead_chicken = IntegerField ("Number of dead chickens")
    submit = SubmitField("Post")
