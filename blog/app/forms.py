from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo, Length
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):      #default naming validate_<parameter> calls automatically 
        user = User.query.filter_by(username=username.data).first()
        if user != None:
            raise ValidationError('Please use a different username')
    
    def validate_email(self, email):
        user_email = User.query.filter_by(email=email.data).first()
        if user_email != None:
            raise VaildationError('Please use a different email address.')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=144)])
    submit =SubmitField('Submit')

class CreatePostForm(FlaskForm):
    text = TextAreaField('Post', validators=[Length(min=10, max=250)])
    submit = SubmitField('Submit')

class AddCommentForm(FlaskForm):
    text = TextAreaField('Comment', validators=[Length(min=5, max=200)])
    submit = SubmitField('Submit')

class AddReplyForm(FlaskForm):
    text = TextAreaField('Reply', validators=[Length(min=2, max=100)])
    submit = SubmitField('Submit')

class EditCommentForm(FlaskForm):
    text = TextAreaField('Edit', validators=[Length(min=2, max=100)])
