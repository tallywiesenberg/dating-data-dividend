from flask import Blueprint, flash, render_template, redirect, jsonify, url_for, render_template_string
from flask_login import login_required, logout_user, current_user, login_user
import requests

from .extensions import db, login_manager, lillith
from .forms import SignUpForm, LoginForm
from .swipe_queue import SwipeQueue
from .tables import User

auth_bp = Blueprint(
    'auth_bp',
    __name__,
    template_folder='templates',
    static_folder='static'
)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():

    #Bypass if user is already signed in
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.home'))
    form = SignUpForm()   
    if form.validate_on_submit():
        #check if user exists in system already
        existing_user = User.query.filter_by(username=form.username.data).first()
        #if the user isn't there yet
        if existing_user is None:
            user = User(
                username = form.username.data,
                address = 'pre-metamask',
                left_swipes_given = 0,
                right_swipes_given = 0,
                matches = 0,
                bio = '',
                time_logged = 0,
                gender = form.gender.data,
                gender_preference = form.gender_preference.data
            )
            #Hash password for protection
            user.set_password(form.password.data)
            #Add new user to database
            db.session.add(user)
            db.session.commit()
            #Create unique swipe queue for user
            session[current_user.username + '_queue'] = SwipeQueue(user)
            session[current_user.username + '_matches']  = []
            #Create user on blockchain
            if user.gender == 'Male':
                lillith.functions.newUser(user.address, 0).call() #0 means gender.male in contract
            if user.gender == 'Female':
                lillith.functions.newUser(user.address, 1).call() #1 means gender.female in contract
            #Login user
            login_user(user)
            
            return redirect(url_for('main_bp.edit_profile'))
        flash('Shoot! That username already exists...')

    # return render_template('register.html', form = form)
    return render_template('register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    #Bypass if user is already signed in
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.home'))

    form = LoginForm()
    #Attempt to validate login attempt
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(password=form.password.data):
            
            login_user(user, remember=form.remember_me.data)

            return redirect(url_for('main_bp.home'))


        flash(f"Sorry...that username/password combination wasn't valid")


    return render_template('login.html', title='Sign In', form=form)
    # return render_template('login.html', title='Sign In', form=form)

@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(int(user_id))
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth_bp.login'))

@auth_bp.route('/')
def redirect_to_home():
    return redirect(url_for('auth_bp.login'))

def render_s3_template(html_file_name):
    '''
    Read jinja template from s3.
    Params:
    html_file_name (str): Pre-S3 name of template

    Returns:
    template_str (str): Html template in string
    '''
    # s3 = boto3.resource(
    #     's3',
    #     aws_access_key=config('AWS_ACCESS_KEY'),
    #     aws_secret_access_key=config('AWS_SECRET_KEY')
    #     )
    # obj = s3.Object(config('BUCKET_NAME'))
    # template_string = obj.get()['templates'][html_file_name].read().decode('utf-8')
    # return template_string

    r = requests.get(f'https://jane-protocol.s3.amazonaws.com/templates/{html_file_name}')
    return r.text