from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, NoneOf
from app.models import get_usernames


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('Please enter your username.')], render_kw={'class': 'form-control', 'required': True, 'autocomplete': 'username', 'maxlength': '25'})
    password = PasswordField('Password', validators=[DataRequired('Please enter your password.')], render_kw={'class': 'form-control', 'required': True, 'autocomplete': 'current-password'})
    remember = BooleanField('remember me', default=False, id="rememberMe")
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('Please enter a username.'), NoneOf(get_usernames())], render_kw={'class': 'form-control', 'required': True, 'maxlength': '25'})
    password = PasswordField('Password', validators=[DataRequired('Please enter a strong password.')], render_kw={'class': 'form-control', 'required': True})
    confirm = PasswordField('Confirm password', validators=[DataRequired('Please match the above password.')], render_kw={'class': 'form-control', 'required': True})
    agree = BooleanField('I agree to the Terms & Conditions', validators=[DataRequired('Please agree to the terms and conditions.')], default=False, id="agree", render_kw={'required': True})
    submit = SubmitField('Create my account')


class RenameForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('Please enter a username.'), NoneOf(get_usernames())], render_kw={'class': 'form-control', 'required': True, 'maxlength': '25'})
    submit = SubmitField('Save Changes')
