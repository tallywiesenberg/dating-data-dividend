from flask import Flask
from decouple import config

from . import auth, routes
from .extensions import db, login_manager, ma, migrate, s3
from .swipe_queue import SwipeQueue

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URI')
    app.config['SECRET_KEY'] = config('SECRET_KEY')
    app.config['FLASKS3_BUCKET_NAME'] = config('BUCKET_NAME')
    app.config['AWS_ACCESS_KEY_ID'] = config('AWS_ACCESS_KEY')
    app.config['AWS_SECRET_ACCESS_KEY'] = config('AWS_SECRET_KEY')

    #Intialize plugins/extensions
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(db)
    login_manager.init_app(app)
    s3.init_app(app)

    #Register blueprints
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(routes.main_bp)

    return app

if __name__ == '__main__':
    my_app = create_app()
    s3.create_all(my_app)
    my_app.run(debug=True)