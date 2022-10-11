from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

from flask_login import current_user
from application.models import User

class LoginForm(FlaskForm):
    email = StringField('אימייל', validators=[DataRequired(), Email()])
    password = PasswordField('סיסמא', validators=[DataRequired()])
    submit = SubmitField('התחברות')

class RegistationForm(FlaskForm):
    email = StringField('אימייל', validators=[DataRequired(), Email()])
    username = StringField('שם משתמש', validators=[DataRequired()])
    password = PasswordField('סיסמא', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')])
    pass_confirm = PasswordField('אימות סיסמא', validators=[DataRequired()])
    first_name = StringField('שם פרטי', validators=[DataRequired()])
    last_name = StringField('שם משפחה', validators=[DataRequired()])
    phone = StringField('מספר פלאפון', validators=[DataRequired()])
    submit = SubmitField("הרשמה")

    def check_email(self, field):
        if User.query.filter_by(email=filed.data).first():
            raise ValidationError('מישהו אחר כבר נרשם עם האימייל שלך')

    def check_username(self, field):
        if User.query.filter_by(username=filed.data).first():
            raise ValidationError('מישהו אחר כבר נרשם עם שם משתמש זה')

class UpdateUserForm(FlaskForm):
    first_name = StringField('שם פרטי', validators=[DataRequired()])
    last_name = StringField('שם משפחה', validators=[DataRequired()])
    email = StringField('אימייל', validators=[DataRequired(), Email()])
    phone = StringField('מספר פלאפון', validators=[DataRequired()])
    username = StringField('שם משתמש', validators=[DataRequired()])
    picture = FileField('עדכן תמונת פרופיל', validators=[FileAllowed(['jpg','png','jpeg','gif'])])
    submit = SubmitField("עדכון")
