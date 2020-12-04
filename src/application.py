from decouple import config
from flask import Flask

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
    db.init_app(application)
    ma.init_app(application)
    migrate.init_app(application)
    login_manager.init_app(application)

    #Register blueprints
    application.register_blueprint(auth.auth_bp)
    application.register_blueprint(routes.main_bp)

    return application

if __name__ == '__main__':
    application = create_app()
    application.static_folder = 'static'
    application.run(debug=True)