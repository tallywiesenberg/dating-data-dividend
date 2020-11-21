from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserLogin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(44), unique=True, nullable=False)
    # data = db.relationship('UserData', backref='user_login')
    # swipes = db.relationship('Swipe', backref='user_login', lazy=True)

    def __repr__(self):
        return f'{self.id} -- {self.username} -- {self.password} -- {self.address}'

class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=True)
    left_swipes = db.Column(db.Integer, nullable=False)
    right_swipes = db.Column(db.Integer, nullable=False)
    matches = db.Column(db.Integer, nullable=False)
    bio = db.Column(db.String(240))
    photos = db.Column(db.PickleType, nullable=False)
    user_id = db.Column(db.String(44),
    #  db.ForeignKey('user_login.id'),
      nullable=False)

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