from flask import Flask
from decouple import config

from . import auth, routes
from .extensions import db, login_manager, ma, migrate
from .swipe_queue import SwipeQueue

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URI')
    app.config['SECRET_KEY'] = config('SECRET_KEY')
    app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
    app.config['MAX_CONTENT_LENGTH'] = 2048 * 2048

    #Intialize plugins/extensions
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(db)
    login_manager.init_app(app)

    #Register blueprints
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(routes.main_bp)

    return app

if __name__ == '__main__':
    my_app = create_app()
    my_app.run(debug=True)