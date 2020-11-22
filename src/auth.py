from flask import Blueprint, flash, render_template, redirect, jsonify, url_for
from flask_login import login_required, logout_user, current_user, login_user, login_manager

from .extensions import db
from .login import SignUpForm, LoginForm
from .tables import UserLogin

auth_bp = Blueprint(
    'auth_bp',
    __name__,
    template_folder='templates',
    static_folder='static'
)

@auth_bp.route('/register', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()   
    if form.validate_on_submit():
        #check if user exists in system already
        existing_user = UserLogin.query.filter_by(username=form.username.data).first()
        #if the user isn't there yet
        if existing_user is None:
            user = UserLogin(
                username = form.username.data,
                address = 'pre-metamask'
            )
            #Hash password for protection
            user.set_password(form.password.data)
            #Add new user to database
            db.session.add(user)
            db.session.commit()
            #Login user
            login_user(user)

            return redirect(url_for('main_bp.home'))
        flash('Shoot! That username already exists...')

    return render_template('signup.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    #Bypass if user is already signed in
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.home'))

    form = LoginForm()
    #Attempt to validate login attempt
    if form.validate_on_submit():
        user = UserLogin.query.filter_by(username=form.username.data)
        if user and user.check_password(password=form.password.data):
            login_user(user)


        flash(f"Sorry...that username/password combination wasn't valid")

        return redirect(url_for('main_bp.home'))

    return render_template('login.html', title='Sign In', form=form)

@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth_bp.login'))