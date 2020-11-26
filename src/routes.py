import boto3
from decouple import config
from flask import Blueprint, flash, render_template, redirect, jsonify, url_for, render_template_string
from flask_login import login_required, current_user, logout_user
import requests

from .auth import render_s3_template
from .login import LoginForm
from .photos import Photos
from .schema import UserLoginSchema, UserDataSchema, Swipe
from .tables import UserData, UserLogin, Swipe, db

main_bp = Blueprint(
    'main_bp',
    __name__,
    template_folder='templates',
    static_folder='static'
)

@main_bp.route('/home')
@login_required
def home():
    # return render_template('home.html')
    return render_template_string(render_s3_template('home.html'))

@main_bp.route('/user/<user_id>')
@login_required
def user(user_id):
    user = UserLogin.query.filter_by(id=user_id).first_or_404()
    user_data = UserData.query.filter_by(user_id=user_id)
    parent_path = user_data.path_to_photos
    s3_photos = Photos(parent_path)
    child_paths = s3_photos.get_paths_to_photos(user_id)
    # return render_template('show_profile.html', user=user, child_paths=child_paths)
    return render_template_string('show_profile.html', user=user, child_paths=child_paths)

@main_bp.route('/user/<user_id>/edit')
@login_required
def edit_profile(user_id):

    # return render_template('edit_profile.html')
    return render_template_string(render_s3_template('edit_profile.html'))

@main_bp.route('/swipe')
@login_required
def swipe():
    user_login_schema = UserLoginSchema(many=True)
    users = UserLogin.query.all()
    return jsonify(user_login_schema.dump(users))

@main_bp.route('/metamask-setup')
@login_required
def metamask_setup():
    pass

@main_bp.route('/no-more-users')
@login_required
def no_more_users():
    # return render_template('no_more_users.html')
    return render_template_string(render_s3_template('no_more_users.html'))

@main_bp.route('/create')
def create_db():
    db.drop_all()
    db.create_all()
    user = UserLogin(username='Tally', password='test', address='0xA97cd82A05386eAdaFCE2bbD2e6a0CbBa7A53a6c')
    db.session.add(user)
    db.session.commit()
    return 'DB created!'

@main_bp.route('/logout')
@login_required
def logout():
    '''user logout logic'''
    logout_user()
    redirect(url_for('auth_bp.login'))
