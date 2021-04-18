from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    logons = db.relationship('Logon', backref='logged_user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username) 


class Logon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(32))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Logon {}>'.format(self.timestamp)