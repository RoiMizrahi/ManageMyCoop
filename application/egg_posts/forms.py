from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms.validators import DataRequired

class EggPostForm(FlaskForm):
    eggs_amount = IntegerField("Number of eggs collected", validators=[DataRequired()])
    broken_eggs = IntegerField("Number of broken eggs collected", validators=[DataRequired()])
    current_food = IntegerField ("Amount of food", validators=[DataRequired()])
    dead_chicken = IntegerField ("Number of dead chickens", validators=[DataRequired()])
    submit = SubmitField("Post")
