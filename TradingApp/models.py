from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    btc_balance = db.Column(db.Integer)
    eth_balance = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Balance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    balances = db.relationship('Balance')
    assets = db.relationship('Asset')
    


