import json

import boto3
from decouple import config
from flask import Blueprint, flash, render_template, redirect, request, jsonify, url_for, render_template_string
from flask_login import login_required, current_user, logout_user
import pandas as pd
import requests

from .auth import render_s3_template
from .login import LoginForm, EditProfileForm
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
    return render_template('home.html')
    # return render_template_string(render_s3_template('home.html'))

@main_bp.route('/user/<username>')
@login_required
def user(username):
    user = UserLogin.query.filter_by(username=username).first_or_404()
    user_data = UserData.query.filter_by(user_id=user.id)
    s3_photos = Photos(username)
    child_paths = s3_photos.get_paths_to_photos(username)
    return render_template('show_profile.html', user=user, child_paths=child_paths, s3_photos = s3_photos)
    # return render_template_string('show_profile.html', user=user, child_paths=child_paths)

@main_bp.route('/user/<username>/edit', methods=['GET', 'POST'])
@login_required
def edit_profile(username):
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.data.username
        current_user.bio = form.data.bio
        db.session.commit()
        #TODO update photo bucket on S3
        for uploaded_file in request.files.getlist('file')
            if uploaded_file.filename != '':
                photos = Photos(username)
                photos.upload_to_s3(uploaded_file)
        flash('Cool...your changes have been saved!')
        return redirect(url_for('main_bp.user'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.bio.data = current_user.bio

    return render_template('edit_profile.html', form=form)
    # return render_template_string(render_s3_template('edit_profile.html'))

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

@main_bp.route('/reset')
def create_db():
    db.drop_all()
    db.create_all()
    users = [UserLogin(username='Tally', password='test', address='0xA97cd82A05386eAdaFCE2bbD2e6a0CbBa7A53a6c')]
    with open('MOCK_DATA.json') as f:
        data = json.loads(f.read())
    for i in data:
        user = UserLogin(username=i['username'], password=i['password'], address=i['address'])
        users.append(user)
    for user in users:
        user.set_password(user.password)
    db.session.add_all(users)
    db.session.commit()
    return 'DB created!'

@main_bp.route('/logout')
@login_required
def logout():
    '''user logout logic'''
    logout_user()
    redirect(url_for('auth_bp.login'))
