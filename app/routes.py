from app import app
from app.forms import LoginForm
from app.errors import not_found_error
from app.models import Users

from flask import render_template, flash, redirect, url_for, request, send_file, make_response
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@app.route('/')
def index():
    # Returns the content of index.html, with the title 'Home'
    if current_user.is_authenticated:
        return render_template('index.html', title='Home'), 200

    # Redirects the user to the login page
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Creates a new login form
    form = LoginForm()

    # Validates login form on POST only
    if form.validate_on_submit():
        # Finds the username from the database
        user = Users.query.filter_by(username=form.username.data).first()

        # If the username or password is invalid, send a message
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password.')
            return redirect(url_for('login'))

        # If successful, log the user in
        login_user(user, remember=form.remember.data)

        # Redirect the user to the page they wanted to reach
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '' or next_page == '/logout':
            next_page = url_for('index')
        return redirect(next_page)

    # Return the content of login.html on GET only
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/favicon.ico')
def favicon():
    return ''
