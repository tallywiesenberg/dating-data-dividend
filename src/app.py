from flask import Flask, flash, render_template, redirect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from decouple import config

from .login import LoginForm
from .model import UserData, UserLogin, Swipe, db
from .swipe_queue import SwipeQueue

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URI')
    app.config['SECRET_KEY'] = config('SECRET_KEY')
    db.init_app(app)

    migrate = Migrate(db)

    @app.route('/')
    def home():
        user = UserLogin(username='Tally', password='test', address='0xA97cd82A05386eAdaFCE2bbD2e6a0CbBa7A53a6c')
        db.session.add(user)
        db.session.commit()
        render_template('home.html', user=user)
        sq = SwipeQueue(user)
        return sq.swipe()

    @app.route('/swipe')
    def swipe():
        return render_template('swipe.html')

    @app.route('/metamask-setup')
    def metamask_setup():
        pass

    @app.route('/no-more-users')
    def no_more_users():
        return render_template('no_more_users.html')

    @app.route('/profile')
    def profile():
        return render_template('profile_editor.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = form.username.data
            flash(f'Hi {user}!')
            return redirect('/')
        return render_template('login.html', title='Sign In', form=form)

    @app.route('/create')
    def create_db():
        db.drop_all()
        db.create_all()
        return 'DB created!'

    return app

if __name__ == '__main__':
    my_app = create_app()
    my_app.run(debug=True)