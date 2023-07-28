from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length


class RegForm(FlaskForm):
    username = StringField('UserName', validators=[DataRequired(), Length(4, 20)])
    email = StringField('email',  validators=[InputRequired(), Length(max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=20)])
    submit = SubmitField('Create Account')

class LoginForm(FlaskForm):
    username = StringField('UserName', validators=[DataRequired(), Length(4, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(10, 100)])
    submit = SubmitField('login')
