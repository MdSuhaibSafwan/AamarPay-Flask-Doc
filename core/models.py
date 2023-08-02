import secrets
from core import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(1000), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, )

    def __repr__(self):
        return "<User %r>" % self.username


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(100), unique=True, nullable=False, default=secrets.token_hex)
    
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), nullable=False)
    description = db.Column(db.Text)
    customer_name = db.Column(db.String(100),)
    customer_email = db.Column(db.String(100),)
    customer_address1 = db.Column(db.Text)
    customer_address2 = db.Column(db.Text)
    customer_city = db.Column(db.String(100),)
    customer_state = db.Column(db.String(100),)
    customer_postcode = db.Column(db.String(100),)
    customer_country = db.Column(db.String(100),)
    customer_phone = db.Column(db.String(100),)
    
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user_transactions = db.relationship('User', backref=db.backref('transactions', lazy=True))

    def __repr__(self):
        return "<Transaction %r>" % self.transaction_id



class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "<Product: %r>" % self.title

