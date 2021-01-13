from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .extensions import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(44), unique=True, nullable=False)
    left_swipes_given = db.Column(db.Integer, nullable=False)
    right_swipes_given = db.Column(db.Integer, nullable=False)
    matches = db.Column(db.Integer, nullable=False)
    bio = db.Column(db.String(240))
    time_logged = db.Column(db.Float, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    gender_preference = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'{self.id} -- {self.username} -- {self.password} -- {self.address}'

    def set_password(self, password):
      '''Create hashed password'''
      self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
      return check_password_hash(self.password, password)

    def set_address(self, address):
      '''Set address from placeholder to real-deal after connecting with metamask'''
      self.address = address

# class UserData(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     left_swipes_given = db.Column(db.Integer, nullable=False)
#     right_swipes_given = db.Column(db.Integer, nullable=False)
#     matches = db.Column(db.Integer, nullable=False)
#     bio = db.Column(db.String(240))
#     path_to_photos = db.Column(db.String(20), nullable=False)
#     user_id = db.Column(db.String(44),
#     #  db.ForeignKey('user_login.id'),
#       nullable=False)

class Swipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    decision = db.Column(db.Boolean, nullable=False)
    #The user that swipes
    front_user = db.Column(db.String(44),
    #  db.ForeignKey('user_login.id'),
      nullable=False)
    #The user that is swiped upon
    back_user = db.Column(db.String(44),
    #  db.ForeignKey('user_login.id'),
      nullable=False)
    match = db.Column(db.Boolean, nullable=False)