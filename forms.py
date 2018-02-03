import flask
from flask_wtf import Form, FlaskForm
import wtforms
from wtforms import validators
from database import db_session, User, Company


class LoginForm(Form):

    email = wtforms.StringField(
        validators=[validators.DataRequired(), validators.Email()],
        description='Email address')

    password = wtforms.PasswordField(
        validators=[validators.DataRequired()],
        description='Password')


class UserInputForm(FlaskForm):

    telegram_id = wtforms.StringField(
        validators=[validators.DataRequired()],
        description='Telegram id')

    last_name = wtforms.StringField(
        validators=[validators.DataRequired()],
        description='User name')

    email = wtforms.StringField(
        validators=[validators.DataRequired(), validators.Email()],
        description='Email address')

    password = wtforms.PasswordField(
        validators=[validators.DataRequired()],
        description='Password')


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


class AgreementInputForm(FlaskForm):

    def __init__(self):
        super(AgreementInputForm, self).__init__()
        self.client_1.choices = [(0, '-----')] + db_session.query(
            Company.id, Company.company_name
        ).order_by(Company.company_name).all()
        self.client_2.choices = self.client_1.choices

    client_1 = wtforms.SelectField("Client 1", coerce=int)
    client_2 = wtforms.SelectField("Client 2", coerce=int)

    agreement = wtforms.StringField(
        validators=[validators.DataRequired()],
        description='Agreement number')

    trade_volume = wtforms.PasswordField(
        validators=[validators.DataRequired()],
        description='Trade volume')
