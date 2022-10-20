from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, NoneOf
from app.models import get_usernames


class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired('Please enter your username.')], render_kw={'class': 'form-control field-top', 'required': True, 'autocomplete': 'username', 'maxlength': '25'})
    password = PasswordField('Password:', validators=[DataRequired('Please enter your password.')], render_kw={'class': 'form-control field-bot', 'required': True, 'autocomplete': 'current-password'})
    remember = BooleanField('Remember me', default=False, id="rememberMe")
    submit = SubmitField('Sign in')


class RegisterForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired('Please enter a username.'), NoneOf(get_usernames())], render_kw={'class': 'form-control field-top', 'required': True, 'maxlength': '25'})
    password = PasswordField('Password:', validators=[DataRequired('Please enter a strong password.')], render_kw={'class': 'form-control field-mid', 'required': True})
    confirm = PasswordField('Confirm password:', validators=[DataRequired('Please match the above password.')], render_kw={'class': 'form-control field-bot', 'required': True})
    submit = SubmitField('Create account')
