from flask_marshmallow import Marshmallow
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_s3 import FlaskS3


db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
s3 = FlaskS3()