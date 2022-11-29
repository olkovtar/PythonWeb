from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo, ValidationError
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
