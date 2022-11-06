from sqlalchemy.sql import functions

from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login.user_loader
def load_user(uid):
    return Users.query.get(int(uid))


class Roles(db.Model):
    __tablename__ = "roles"
    user_id = db.Column(db.ForeignKey('users.user_id'), primary_key=True)
    list_id = db.Column(db.ForeignKey('lists.list_id'), primary_key=True)
    role = db.Column(db.VARCHAR(25), nullable=False)
    user = db.relationship("Users", back_populates="lists")
    list = db.relationship("Lists", back_populates="users")


class Users(db.Model, UserMixin):
    __tablename__ = "users"
    user_id = db.Column(db.INT, name='user_id', primary_key=True, autoincrement=True)
    username = db.Column(db.VARCHAR(25), name='username', nullable=False, unique=True, index=True)
    password_hash = db.Column(db.CHAR(102), name='password', nullable=False)
    filename = db.Column(db.VARCHAR(50), name='filename', nullable=False, default='default_profile.jpg')
    lists = db.relationship("Roles", back_populates='user', cascade="all, delete-orphan")

    def set_username(self, username):
        if not get_user(username):
            self.username = username
            db.session.commit()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        db.session.commit()

    def set_filename(self, filename):
        self.filename = filename
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(str(self.password_hash).rstrip(), password)

    def get_id(self):
        return self.user_id

    def remove(self):
        db.session.delete(self)
        db.session.commit()


class Lists(db.Model):
    __tablename__ = "lists"
    list_id = db.Column(db.INT, name='list_id', primary_key=True, autoincrement=True)
    created = db.Column(db.TIMESTAMP, name='created', nullable=False, index=True, default=functions.current_timestamp())
    title = db.Column(db.VARCHAR(25), name='title', nullable=False)
    content = db.Column(db.JSON, name='content', nullable=False)
    category = db.Column(db.VARCHAR(25), name='category', nullable=False, default='default')
    users = db.relationship("Roles", back_populates='list', cascade="all, delete-orphan")

    def set_category(self, category):
        self.category = category
        db.session.commit()


# ---------- API ----------
# User queries
def add_user(username, password):
    user = Users()
    user.set_username(username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()


def get_usernames():
    return db.session.query(Users.username).all()


def get_user(username):
    return Users.query.filter_by(username=username).first()


def get_role(user, list_id):
    return db.session.query(Roles).filter_by(user_id=user.user_id).filter_by(list_id=list_id).first()


# List queries
def __get_list_query(user, columns):
    return db.session.query(columns).join(Roles).filter(Roles.user_id == user.user_id)


def get_categories(user):
    return __get_list_query(user, Lists.category).distinct().order_by(Lists.category.asc()).all()


def get_lists(user, category=None):
    if not category:
        return __get_list_query(user, Lists).all()
    return __get_list_query(user, Lists).filter(Lists.category == category).order_by(Lists.created.desc()).all()


def get_list(user, list_id):
    return __get_list_query(user, Lists).filter(Roles.list_id == list_id).first()


def add_list(user, category):
    a = Roles(role="owner")
    a.list = Lists()
    a.list.title = ""
    a.list.content = ""
    a.list.category = category
    user.lists.append(a)
    db.session.commit()
    return a.list.list_id


def delete_list(user, list_id):
    list = get_list(user, list_id)
    list_ids = [list.list_id for list in user.lists]
    if list.list_id not in list_ids:
        return
    db.session.delete(list)
    db.session.commit()
