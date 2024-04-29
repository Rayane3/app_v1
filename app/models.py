from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_of_reservation = db.Column(db.Date, nullable=False)
    time_of_reservation = db.Column(db.Time, nullable=False)
    end_time_of_reservation = db.Column(db.Time, nullable=False)
    booked_place = db.Column(db.String(50), nullable=False)
    user = db.relationship('User', backref=db.backref('reservations', lazy=True))

