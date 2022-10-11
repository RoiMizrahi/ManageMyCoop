from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms.validators import DataRequired

class EggPostForm(FlaskForm):
    eggs_amount = IntegerField("כמות ביצים שלמות")
    broken_eggs = IntegerField("כמות ביצים שבורות")
    current_food = IntegerField ("כמות אוכל עדכנית")
    dead_chicken = IntegerField ("כמות תרנגולות מתות")
    submit = SubmitField("שליחה")
