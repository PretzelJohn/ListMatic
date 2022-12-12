import uuid

from app import app
from app.forms import LoginForm, RegisterForm, RenameForm
from app.errors import not_found_error
from app.models import *
from app.s3 import s3_upload, s3_delete

from flask import render_template, flash, redirect, url_for, request, make_response
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


# ---------- Website ----------
# Landing page
@app.route('/')
def index():
    return render_template('index.html')


# Dashboard - shows all lists
@app.route('/dashboard')
@login_required
def dashboard():
    categories = [category[0] for category in get_categories(current_user)]
    if not categories:
        categories = ["Default"]
    lists = get_lists(current_user)

    return render_template('dashboard.html', title='Home', lists=lists, categories=categories, get_lists=get_lists, get_role=get_role, str=str)


# Creates a new category
@app.route('/create/<string:category>', methods=['GET'])
@login_required
def list_create(category):
    list_id = add_list(current_user, category)
    flash('You have created a new list!', 'success')
    return redirect(url_for('list_view', list_id=list_id))


# Shows a specific list
@app.route('/<int:list_id>')
@login_required
def list_view(list_id):
    role_obj = get_role(current_user, list_id)

    if not role_obj:
        return not_found_error('')

    list_obj = get_list(current_user, list_id)
    if not list_obj:
        return not_found_error('')

    print(list_obj, role_obj.role)
    return render_template('list.html', list=list_obj, role=role_obj.role)


# Updates a list
@app.route('/<int:list_id>/update', methods=['GET', 'POST'])
@login_required
def list_update(list_id):
    if request.method != 'POST':
        return redirect(url_for('list_view', list_id=list_id))

    role = get_role(current_user, list_id)
    if role and role.role not in ['owner', 'editor']:
        return redirect(url_for('list_view', list_id=list_id))

    try:
        data = request.get_json()
        list = get_list(current_user, list_id)
        list.set_title(data["title"])
        list.set_content(data["content"])
        return make_response('Success', 200)
    except Exception as e:
        return make_response(e, 200)


# Changes the category of a list
@app.route('/<int:list_id>/change', methods=['GET', 'POST'])
@login_required
def list_change(list_id):
    if request.method != 'POST':
        return redirect(url_for('dashboard'))

    role = get_role(current_user, list_id)
    if role and role.role not in ['owner', 'editor']:
        return redirect(url_for('dashboard'))

    category = request.form.get("selectedCategory")
    if category == "new":
        if request.form.get("newCategoryText"):
            category = request.form.get("newCategoryText")
        else:
            flash('You must specify the name of the new category!', 'danger')
            return redirect(url_for('dashboard'))

    list = get_list(current_user, list_id)
    if category == list.category:
        flash('The list was already in the '+category+' category.', 'danger')
    else:
        list.set_category(category)
        flash('You have moved the list to the '+category+' category!', 'success')

    return redirect(url_for('dashboard'))


# Deletes a list
@app.route('/<int:list_id>/delete/', methods=['GET', 'POST'])
@login_required
def list_delete(list_id):
    if request.method != 'POST':
        return redirect(url_for('dashboard'))

    role = get_role(current_user, list_id)
    if role and role.role not in 'owner':
        return redirect(url_for('dashboard'))

    delete_list(current_user, list_id)
    flash('You have deleted the list!', 'success')
    return redirect(url_for('dashboard'))


# Deletes a list that the user doesn't own
@app.route('/<int:list_id>/delete_role', methods=['GET', 'POST'])
@login_required
def role_delete(list_id):
    if request.method != 'POST':
        return redirect(url_for('dashboard'))

    role = get_role(current_user, list_id)
    if role and role.role in 'owner':
        return redirect(url_for('dashboard'))

    delete_role(current_user, list_id)
    flash('You have deleted the list!', 'success')
    return redirect(url_for('dashboard'))


# ---------- User account ----------
# Returns the file's extension (jpg, png)
def get_extension(filename):
    return filename.rsplit('.', 1)[1].lower()


# Returns true if the image file is valid
def validate_image(filename):
    return '.' in filename and get_extension(filename) in ['jpg', 'png']


# Returns the account info page
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    # Creates a new registration form
    form = RenameForm()

    # Validates registration form on POST only
    if form.validate_on_submit():
        # If the username has been taken, send a message
        if get_user(form.username.data):
            flash('That username already exists!', 'danger')
            return redirect(url_for('account'))

        # If successful, change the username
        current_user.set_username(form.username.data)

        # Redirect the user to the login page
        flash('Username updated successfully!', 'success')

    return render_template('account.html', form=form)


# Handles account deletes
@app.route('/account/delete', methods=['GET', 'POST'])
@login_required
def account_delete():
    if request.method != 'POST':
        return redirect(url_for('account'))

    current_user.remove()
    flash('Your account was deleted successfully!', 'success')
    return redirect(url_for('login'))


# Handles profile picture updates
@app.route('/profile/update', methods=['GET', 'POST'])
@login_required
def profile_edit():
    if request.method != 'POST':
        return redirect(url_for('account'))

    if 'file' not in request.files:
        flash('No file selected!', 'danger')

    file = request.files['file']
    filename = file.filename
    mimetype = request.mimetype

    if not file or not filename:
        flash('No file selected!', 'danger')
    elif validate_image(filename):
        if current_user.filename != 'default_profile.jpg':
            s3_delete(current_user.filename)

        filename = uuid.uuid4().hex + '.' + get_extension(filename)
        current_user.set_filename(filename)
        s3_upload(file, current_user.filename, mimetype)
        flash('Updated your profile picture successfully!', 'success')
    else:
        flash('That file type is not allowed! Please upload a valid .jpg or .png image.', 'danger')

    return redirect(url_for('account'))


# Handles profile picture deletes
@app.route('/profile/delete', methods=['GET', 'POST'])
@login_required
def profile_delete():
    if request.method != 'POST':
        return redirect(url_for('account'))

    if current_user.filename != 'default_profile.jpg':
        s3_delete(current_user.filename)
    current_user.set_filename('default_profile.jpg')
    flash('Removed your profile picture successfully!', 'success')
    return redirect(url_for('account'))


# ---------- User login ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user and current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    # Creates a new login form
    form = LoginForm()

    # Validates login form on POST only
    if form.validate_on_submit():
        # Finds the username from the database
        user = get_user(form.username.data)

        # If the username or password is invalid, send a message
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('login'))

        # If successful, log the user in
        login_user(user, remember=form.remember.data)

        # Redirect the user to the page they wanted to reach
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '' or next_page == '/logout':
            next_page = url_for('dashboard')
        return redirect(next_page)

    # Return the content of login.html on GET only
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Creates a new registration form
    form = RegisterForm()

    # Validates registration form on POST only
    if form.validate_on_submit():
        # If the username has been taken, send a message
        if get_user(form.username.data):
            flash('That username already exists!', 'danger')
            return redirect(url_for('register'))

        # If the password doesn't match, send a message
        if form.password.data != form.confirm.data:
            flash('The passwords don\'t match. Please try again.', 'danger')
            return redirect(url_for('register'))

        # If successful, create a new account
        add_user(form.username.data, form.password.data)

        # Redirect the user to the login page
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Create Account', form=form)
