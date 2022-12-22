from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo, ValidationError
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from .models import User


class RegistrationForm(FlaskForm):

    username = StringField("Username", validators=[DataRequired(),
                                                   Length(min=4, max=10,
                                                          message='Length of this field must be between 4 and 10'),
                                                   Regexp(regex='^[A-Za-z][A-Za-z0-9_.]*$')])

    email = StringField("Email", validators=[DataRequired(),
                                             Email(message='Enter correct email')])

    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(min=6, message="Password must be longer than 6 symbols")])

    confirm_password = PasswordField('Confirm password',
                                     validators=[DataRequired("Confirm your password"),
                                                 EqualTo("password")])

    submit = SubmitField("Sign up")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use')


class LoginForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(),
                                             Email("Invalid email")])

    password = PasswordField('Password', [DataRequired()])

    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):

    username = StringField("Username", validators=[DataRequired(""),
                                                   Length(min=4, max=10,
                                                          message='Length of this field must be between 4 and 10')])

    email = StringField('Email', validators=[DataRequired(),
                                             Email("Enter correct email")])

    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

    about_me = TextAreaField("About me", validators=[Length(max=150, message='max length is 150')])

    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            if User.query.filter_by(username=username.data).first():
                raise ValidationError('This username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            if User.query.filter_by(email=email.data).first():
                raise ValidationError('This email is taken. Please choose a different one.')


class ResetPasswordForm(FlaskForm):

    old_password = PasswordField('Old password')

    new_password = PasswordField('New password',
                                 validators=[Length(min=6, message="Password must be longer than 6 symbols")])

    confirm_password = PasswordField('Confirm new password', validators=[DataRequired(), EqualTo("new_password")])

    submit = SubmitField("Reset password")

    def validate_old_password(self, old_password):
        if not current_user.verify_password(old_password.data):
            raise ValidationError('Wrong password. Try again!')
