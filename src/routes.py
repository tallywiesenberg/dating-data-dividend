from flask import Blueprint, flash, render_template, redirect, jsonify, url_for
from flask_login import login_required, current_user, logout_user

from .login import LoginForm
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

@main_bp.route('/swipe')
@login_required
def swipe():
    user_login_schema = UserLoginSchema(many=True)
    users = UserLogin.query.all()
    return jsonify(user_login_schema.dump(users))

@main_bp.route('/metamask-setup')
def metamask_setup():
    pass

@main_bp.route('/no-more-users')
def no_more_users():
    return render_template('no_more_users.html')

@main_bp.route('/profile')
def profile():
    return render_template('profile_editor.html')

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