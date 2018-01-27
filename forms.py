import flask
from flask_wtf import Form, FlaskForm
import wtforms
from wtforms import validators

class LoginForm(Form):

    email = wtforms.StringField(
        validators=[validators.DataRequired(), validators.Email()],
        description='Email address')

    password = wtforms.PasswordField(
        validators=[validators.DataRequired()],
        description='Password')

class UserInputForm(Form):

    telegram_id = wtforms.StringField(
        validators=[validators.DataRequired()],
        description='Telegram id')

    user_name = wtforms.StringField(
        validators=[validators.DataRequired()],
        description='User name')

    email = wtforms.StringField(
        validators=[validators.DataRequired(), validators.Email()],
        description='Email address')

    phone = wtforms.PasswordField(
        validators=[validators.DataRequired()],
        description='Phone number')


class ClientInputForm(FlaskForm):

    itin_num = wtforms.StringField(
        validators=[validators.DataRequired()],
        description='Itin_address')

    company_name = wtforms.StringField(
        validators=[validators.DataRequired()],
        description='Company_name')

    email = wtforms.StringField(
        validators=[validators.DataRequired(), validators.Email()],
        description='Email_address')

    phone_numb = wtforms.PasswordField(
        validators=[validators.DataRequired()],
        description='Phone_number')


class AgreementInputForm(Form):

    client_1 = wtforms.StringField(
        validators=[validators.DataRequired()],
        description='Client 1 name')

    client_2 = wtforms.StringField(
        validators=[validators.DataRequired()],
        description='Client 2 name')

    agreement = wtforms.StringField(
        validators=[validators.DataRequired(), validators.Email()],
        description='Agreement number')

    trade_volume = wtforms.PasswordField(
        validators=[validators.DataRequired()],
        description='Trade volume')