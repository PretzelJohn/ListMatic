from app import app
from app.forms import LoginForm, RegisterForm
from app.errors import not_found_error
from app.models import *

from flask import render_template, flash, redirect, url_for, request, send_file, make_response
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

import os


# ---------- Website ----------
# Homepage - shows all lists?
@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    categories = get_categories(current_user)
    lists = get_lists(current_user)
    return render_template('index.html', title='Home', lists=lists, categories=categories, category='All')


@app.route('/<category>')
@login_required
def category_view(category):
    categories = get_categories(current_user)
    lists = get_lists(current_user, category)
    return render_template('index.html', title='Home', lists=lists, categories=categories, category=category)


@app.route('/<category>/<list_id>')
@login_required
def list_view(category, list_id):
    role_obj = get_role(current_user, list_id)

    if not role_obj:
        return not_found_error('')

    list_obj = get_list(current_user, list_id)
    if not list_obj:
        return not_found_error('')

    print(list_obj, role_obj.role)
    return render_template('list.html', list=list_obj, role=role_obj.role)


# Browser icon
@app.route('/favicon.ico')
def favicon():
    return ''


# ---------- User login ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Creates a new login form
    form = LoginForm()

    # Validates login form on POST only
    if form.validate_on_submit():
        # Finds the username from the database
        user = get_user(form.username.data)

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


@app.route('/signup', methods=['GET', 'POST'])
def register():
    # Creates a new registration form
    form = RegisterForm()

    # Validates registration form on POST only
    if form.validate_on_submit():
        # Finds the username from the database
        user = get_user(form.username.data)

        # If the username has been taken, send a message
        if user:
            flash('That username already exists!')
            return redirect(url_for('register'))

        # If the password doesn't match, send a message
        if form.password.data != form.confirm.data:
            flash('Your password doesn\'t match. Please try again.')
            return redirect(url_for('register'))

        # If successful, create a new account
        add_user(form.username.data, form.password.data)

        # Redirect the user to the login page
        flash('Account created successfully!')
        return redirect(url_for('login'))

    return render_template('register.html', title='Create Account', form=form)
