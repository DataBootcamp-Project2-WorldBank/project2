from datetime import datetime
from hashlib import md5
from time import time
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    logons = db.relationship('Logon', backref='logged_user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username) 

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Logon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(32))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Logon {}>'.format(self.timestamp)
      
class ProjectSummary(db.Model) :
    region            = db.Column(db.String(10))
    country_code_a2   = db.Column(db.String(10), primary_key=True)
    country_code_a3   = db.Column(db.String(10), primary_key=True)
    country_name      = db.Column(db.String(100))
    total             = db.Column(db.Integer)
    satisfactory      = db.Column(db.Integer)
    unsatisfactory    = db.Column(db.Integer)
    unavailable       = db.Column(db.Integer)
    avg_population    = db.Column(db.Integer)

    def __repr__(self):
        return {  "region"          : self.region,
                  "country_code_a2" : self.country_code_a2,
                  "country_code_a3" : self.country_code_a3,
                  "country_name"    : self.country_name,
                  "total"           : self.total,
                  "satisfactory"    : self.satisfactory,
                  "unsatisfactory"  : self.unsatisfactory,
                  "unavailble"      : self.unavailable, 
                  "Avg_Population"  : self.avg_population
            }
       

class ProjectPerformanceRatings(db.Model) :
        project_id        = db.Column("Project ID",   db.String(20) , primary_key=True)
        project_name      = db.Column("Project Name", db.String(100), default="N/A")
        region            = db.Column("region",       db.String(3)  , default="N/A" )
        country_code      = db.Column("Country Code" ,db.String(3)  , default="N/A", primary_key=True)
        country_name      = db.Column("Country Name" ,db.String(100), default=0)
        project_cost      = db.Column("Lending Project Cost", db.Integer, default=0)
        IEG_outcome       = db.Column("ieg_Outcome", db.String     , default="N/A")

        def __repr__(self):
            return {  
                "project_id"        : self.project_id,
                "project_name"      : self.project_name,
                "region"            : self.region,
                "country_code"      : self.country_code,
                "country_name"      : self.country_name,
                "project_cost"      : self.project_cost,
                "ieg_outcome"       : self.IEG_outcome
            }

       
@login.user_loader
def load_user(id):
    return User.query.get(int(id))