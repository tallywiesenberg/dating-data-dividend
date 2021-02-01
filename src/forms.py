from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, MultipleFileField
from wtforms.fields import RadioField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in :)')


class SignUpForm(FlaskForm):
    '''User registration form'''
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, message='a stronger password please!')])
    confirm_password = PasswordField('Confirm password', validators=[
        DataRequired(), EqualTo('password', message='passwords must match. doublecheck your spelling!')
        ])
    address = StringField('Address', validators=[DataRequired()])
    gender = RadioField('Your gender:', choices=[('Male', 'Male'), ('Female', 'Female')], validators=[DataRequired()])
    gender_preference = RadioField('Your gender preference:', choices=[('Male', 'Male'), ('Female', 'Female')], validators=[DataRequired()])
    submit = SubmitField('Register :)')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    bio = StringField('My bio', validators=[Length(max=240)])
    photos = MultipleFileField('Upload photo(s)', validators=[
        FileAllowed(['jpg', 'png', 'gif'], 'Images only!')
    ])
    submit = SubmitField('submit!')

class SwipeForm(FlaskForm):
    swipe_choice = RadioField('You like?', choices=[('Yes', 'I like!'), ('No', 'No thanks..')])