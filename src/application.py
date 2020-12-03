from flask import Flask
from decouple import config

from . import auth, routes
from .extensions import db, login_manager, ma, migrate
from .swipe_queue import SwipeQueue

def create_app():
    application = Flask(__name__)
    application.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URI')
    application.config['SECRET_KEY'] = config('SECRET_KEY')
    application.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
    application.config['MAX_CONTENT_LENGTH'] = 2048 * 2048

    #Intialize plugins/extensions
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(db)
    login_manager.init_app(app)

    #Register blueprints
    application.register_blueprint(auth.auth_bp)
    application.register_blueprint(routes.main_bp)

    return application

if __name__ == '__main__':
    application = create_app()
    application.static_folder = 'static'
    application.run(debug=True)