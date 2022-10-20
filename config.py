import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'\x13\xd0\x18B\x9b\xb5-&\t\x07\xee\xce\xa7\x83\xd1Y'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///'+os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    S3_BUCKET = os.environ.get('S3_BUCKET')
    S3_KEY = os.environ.get('S3_KEY')
    S3_SECRET = os.environ.get('S3_SECRET')
    S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)
