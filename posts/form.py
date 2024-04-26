from flask_login import current_user
from flask_wtf.form import _Auto
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed

from posts.models import User
from posts import bcrypt


class RegisterForm(FlaskForm):
    '''
    Class for register form
    '''
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        '''
        Function to validate username
        '''
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This Username is taken. Please choose a different one.')
        
    def validate_email(self, email):
        '''
        Function to validate email
        '''
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(f'An account with the email {email.data} \
                                  already exists. Please try logging in or choose a different one.')


class LoginForm(FlaskForm):
    '''
    Class for login form
    '''
    email = StringField('Email', validators=[DataRequired(), Email()], description='Email')
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

    def validate_email(self, email):
        '''
        Function to validate email
        '''
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('There is no account with this email. Please register first.')
        
    def validate_password(self, password):
        user = User.query.filter_by(email=self.email.data).first()
        if not (user and bcrypt.check_password_hash(user.password, password.data)):
            raise ValidationError('Login failed. Please check your password and try again.')
        

class UpdateAccountForm(FlaskForm):
    '''
    Class for register form
    '''
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Profile picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Save')

    def validate_username(self, username):
        '''
        Function to validate username
        '''
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This Username is taken. Please choose a different one.')
            
    def validate_email(self, email):
        '''
        Function to validate email
        '''
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(f'An account with the email {email.data} \
                                    already exists. Please try logging in or choose a different one.')
            

class PostForm(FlaskForm):
    '''
    Class for register form
    '''

    action = None

    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=120)])
    content = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField(action if action else 'Post')
