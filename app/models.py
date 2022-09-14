from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login.user_loader
def load_user(id):
    return Users.query.get(int(id))


class Users(db.Model, UserMixin):
    user_id = db.Column(db.INT, name='UserID', primary_key=True)
    username = db.Column(db.CHAR(25), name='Username', index=True, unique=True)
    password_hash = db.Column(db.CHAR(100), name='PasswordHash')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(str(self.password_hash).rstrip(), password)

    def get_id(self):
        return self.user_id

    def __repr__(self):
        return '<User {}>'.format(self.username)
