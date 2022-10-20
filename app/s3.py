import boto3

from app import app


def s3_client():
    session = boto3.session.Session()
    client = session.client('s3', aws_access_key_id=app.config['S3_KEY'], aws_secret_access_key=app.config['S3_SECRET'])
    return client


def s3_delete(filename):
    client = s3_client()
    return client.delete_object(Bucket=app.config['S3_BUCKET'], Key=filename)


def s3_upload(file, filename, mimetype):
    client = s3_client()
    return client.put_object(Body=file, Bucket=app.config['S3_BUCKET'], Key=filename, ContentType=mimetype, ACL="public-read")
