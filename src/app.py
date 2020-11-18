from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from decouple import config

from .model import User, Swipe, db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URI')
    db.init_app(app)

    @app.route('/')
    def home():
        user = {'username': 'Becky'}
        return render_template('home.html', user=user)

    @app.route('/create')
    def create_db():
        db.create_all()

    return app

if __name__ == '__main__':
    my_app = create_app()
    my_app.run(debug=True)