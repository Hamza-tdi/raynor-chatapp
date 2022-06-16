from wtforms import PasswordField, StringField, SubmitField, DateField, EmailField, validators, RadioField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from models import *
from passlib.hash import pbkdf2_sha256


def invalid_credentials(form, field):
    """ username and password checker"""
    full_name = form.full_name.data
    password = field.data

    user = User.query.filter_by(full_name=full_name).first()
    if not user:
        raise ValidationError('Username or Password are invalid')
    elif not pbkdf2_sha256.verify(password, user.password):
        raise ValidationError('Username or Password are invalid')


class RegistrationForm(FlaskForm):
    """ Registration Form"""

    first_name = StringField('first_name_mabel',
                             validators=[InputRequired(message='First name required'),
                                         Length(min=4, max=25, message='Username must be between 4 and 25 character')])
    last_name = StringField('last_name_label',
                            validators=[InputRequired(message='Last name required'),
                                        Length(min=4, max=25, message='Username must be between 4 and 25 character')])
    birth_date = DateField('Date')
    phone_number = StringField('phone_number_label', validators=[InputRequired(message='Phone number required'),
                                                                Length(min=10, max=10,
                                                                message='Phone number must be 10 characters long')])
    email_address = EmailField('email_label', [validators.DataRequired(message='Email Required'),
                                                 validators.Email(message='Please insert valid email')])
    address = StringField('address_label', validators=[InputRequired(message='Address required')])
    zipcode = StringField('address_label', validators=[InputRequired(message='Zipcode required')])
    genre = RadioField('genre', choices=[('Male', 'Male'), ('Female', 'Female')])
    title = StringField('company_title_label', validators=[InputRequired(message='Please Insert Your company title')])
    department = StringField('company_department_label', validators=[InputRequired(message='Please Insert your '
                                                                                           'company department')])
    password = PasswordField('password_label',
                             validators=[InputRequired(message='Password required'),
                                         Length(min=8, max=64, message='Password must be between 8 and 64 character')])
    confirm_pswd = PasswordField('confirm_pswd_label',
                                 validators=[InputRequired(message='Password required'),
                                             Length(min=8, max=64,
                                                    message='Password must be between 8 and 64 character')])
    submit_button = SubmitField('Create')


class LoginForm(FlaskForm):
    full_name = StringField('username_label', validators=[InputRequired(message='Username Required')])
    password = PasswordField('password_label', validators=[InputRequired(message='Password Required'),
                                                           invalid_credentials])

    submit_button = SubmitField('Login')
