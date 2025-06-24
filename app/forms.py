from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2,max=150)])
    password = PasswordField('Password', validators=[DataRequired()])
    admin = BooleanField('Login as Admin')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2,max=150)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

