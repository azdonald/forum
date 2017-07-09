from datetime import datetime
from app import db

class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(100), unique=True)
    body = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now())
    replies = db.relationship('Replies', backref='thread', lazy='dynamic')


class Replies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'))
    body = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now())

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.now())
    threads = db.relationship('Thread', backref='user', lazy='dynamic')
    replies = db.relationship('Replies', backref='user', lazy='dynamic')

