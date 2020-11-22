from flask import Flask, flash, render_template, redirect, jsonify
from decouple import config

from .extensions import db, login_manager, ma, migrate
from .login import LoginForm
from .tables import UserData, UserLogin, Swipe, db
from .schema import UserLoginSchema, UserDataSchema, Swipe
from .swipe_queue import SwipeQueue

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URI')
    app.config['SECRET_KEY'] = config('SECRET_KEY')

    #Intialize plugins/extensions
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(db)
    login_manager.init_app(app)

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/swipe')
    def swipe():
        user_login_schema = UserLoginSchema(many=True)
        users = UserLogin.query.all()
        return jsonify(user_login_schema.dump(users))

    @app.route('/metamask-setup')
    def metamask_setup():
        pass

    @app.route('/no-more-users')
    def no_more_users():
        return render_template('no_more_users.html')

    @app.route('/profile')
    def profile():
        return render_template('profile_editor.html')

    @app.route('/create')
    def create_db():
        db.drop_all()
        db.create_all()
        user = UserLogin(username='Tally', password='test', address='0xA97cd82A05386eAdaFCE2bbD2e6a0CbBa7A53a6c')
        db.session.add(user)
        db.session.commit()
        return 'DB created!'

    return app

if __name__ == '__main__':
    my_app = create_app()
    my_app.run(debug=True)