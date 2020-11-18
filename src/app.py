from flask import Flask, flash, render_template, redirect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from decouple import config

from .login import LoginForm
from .model import UserData, UserLogin, Swipe, db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URI')
    app.config['SECRET_KEY'] = config('SECRET_KEY')
    db.init_app(app)

    migrate = Migrate(db)

    @app.route('/')
    def home():
        user = {'username': 'Becky'}
        return render_template('home.html', user=user)

    @app.route('/metamask-setup')
    def metamask_setup():
        pass



    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = form.username.data
            flash(f'Hi {user}!')
            return redirect('/', user=user)
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