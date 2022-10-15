from app import db, login
from datetime import date
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login.user_loader
def load_user(uid):
    return Users.query.get(int(uid))


roles = db.Table(
    "roles",
    db.Column('user_id', db.INT, db.ForeignKey('users.user_id'), primary_key=True),
    db.Column('list_id', db.INT, db.ForeignKey('lists.list_id'), primary_key=True),
    db.Column('role', db.VARCHAR(25), nullable=False)
)


class Users(db.Model, UserMixin):
    user_id = db.Column(db.INT, name='user_id', primary_key=True, autoincrement=True)
    username = db.Column(db.VARCHAR(25), name='username', nullable=False, unique=True, index=True)
    password_hash = db.Column(db.CHAR(102), name='password', nullable=False)
    lists = db.relationship('Lists', secondary=roles, back_populates='users')

    def set_username(self, username):
        if not get_user(username):
            self.username = username
            db.session.commit()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(str(self.password_hash).rstrip(), password)

    def get_id(self):
        return self.user_id


class Lists(db.Model):
    list_id = db.Column(db.INT, name='list_id', primary_key=True, autoincrement=True)
    created = db.Column(db.TIMESTAMP, name='created', nullable=False, index=True, default=date.today())
    title = db.Column(db.VARCHAR(25), name='title', nullable=False)
    content = db.Column(db.JSON, name='content', nullable=False)
    category = db.Column(db.VARCHAR(25), name='category', nullable=False, default='default')
    users = db.relationship('Users', secondary=roles, back_populates='lists')


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
    return db.session.query(roles).filter_by(user_id=user.user_id).filter_by(list_id=list_id).first()


# List queries
def __get_list_query(user, columns):
    return db.session.query(columns).join(roles).filter(roles.c.user_id == user.user_id)


def get_categories(user):
    return __get_list_query(user, Lists.category).distinct().all()


def get_lists(user, category=None):
    if not category:
        return __get_list_query(user, Lists).all()
    return __get_list_query(user, Lists).filter(Lists.category == category).all()


def get_list(user, list_id):
    return __get_list_query(user, Lists).filter(roles.c.list_id == list_id).first()



