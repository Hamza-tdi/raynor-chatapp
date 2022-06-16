from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User Model"""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32), unique=True, nullable=False)
    last_name = db.Column(db.String(32), unique=True, nullable=False)
    full_name = db.Column(db.String(32), unique=True, nullable=False)
    birth_date = db.Column(db.String(16), nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)
    email_address = db.Column(db.String(32), nullable=False)
    address = db.Column(db.String(64), nullable=False)
    zipcode = db.Column(db.String(12), nullable=False)
    genre = db.Column(db.String(6), nullable=False)
    title = db.Column(db.String(32), nullable=False)
    department = db.Column(db.String(12), nullable=False)
    password = db.Column(db.String(8), nullable=False)
    role = db.Column(db.String(8), nullable=False)
    account_status = db.Column(db.String(8), nullable=False)


class Message(db.Model):
    """Message Model"""
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    message_text = db.Column(db.String(255), nullable=False)
    message_sender = db.Column(db.String(25), nullable=False)
    message_time = db.Column(db.String(25), nullable=False)
    message_room = db.Column(db.String(25), nullable=False)
    message_type = db.Column(db.String(25), nullable=False)


class Room(db.Model):
    """Room Model"""
    __tablename__ = "rooms"
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(25), nullable=False)
    nbr_users = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.String(25), nullable=False)
