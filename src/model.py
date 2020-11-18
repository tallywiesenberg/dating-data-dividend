from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    # address = db.Column(db.String(44), unique=True, nullable=False)
    wallet = db.relationship('Swipe', backref='user', lazy=True)
    score = db.Column(db.Integer, nullable=True)
    left_swipes = db.Column(db.Integer, nullable=False)
    right_swipes = db.Column(db.Integer, nullable=False)
    matches = db.Column(db.Integer, nullable=False)
    bio = db.Column(db.String(240))
    photos = db.Column(db.PickleType, nullable=False)

class Swipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    decision = db.Column(db.Boolean, nullable=False)
    #The user that swipes
    front_user = db.Column(db.String(44), db.ForeignKey('user.wallet'), nullable=False)
    #The user that is swiped upon
    back_user = db.Column(db.String(44), db.ForeignKey('user.wallet'), nullable=False)
    match = db.Column(db.Boolean, nullable=False)