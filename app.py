import flask

app = flask.Flask(__name__)

app.config.update(SECRET_KEY='not very secret')

import requests
import hashlib
import uuid
import sqlalchemy as sa
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin
# from local_settings import TELE_TOKEN, CRM_CHANNEL
from database import db_session, User, Company, Agreements
# from utils import crm_update_message

from flask_login import LoginManager

login_manager = LoginManager()
login_manager.init_app(app)
# Это нужно для того, чтобы модуль login_manager знал куда редиректить пользователя
login_manager.login_view = 'login'


# Требуется для работы модуля flask_login
@login_manager.user_loader
def load_user(email):
    return db_session.query(User).filter(User.email == email).first()

from flask_wtf import Form, FlaskForm
import wtforms
from wtforms import validators

from forms import LoginForm, UserInputForm, ClientInputForm, AgreementInputForm

from flask_login import login_user, logout_user, login_required, current_user
from flask import render_template


@app.route('/', methods=['GET', 'POST'])
@login_required  # Если пользователь не залогинен,
                 # то редирект на страницу логина
def index():
    form_users = UserInputForm()
    if form_users.validate_on_submit():
        user = User(last_name=form_users.last_name.data,
                    email=form_users.email.data,
                    telegram_id=form_users.telegram_id.data)
        user.password = form_users.password.data
        print(user)
        db_session.add(user)
        db_session.commit()
        return flask.redirect(flask.url_for('index'))

    form_clients = ClientInputForm()
    if form_clients.validate_on_submit():
        client = Company(company_name=form_clients.company_name.data,
                         itin_num=form_clients.itin_num.data,
                         email=form_clients.email.data,
                         phone_numb=form_clients.phone_numb.data)
        db_session.add(client)
        db_session.commit()
        flask.flash('DONE!')

        text = 'В базе CRM зарегистрирован новый клиент - {}.\n Контакты:\n Email: {}\n Телефон: {}'.format(form_clients.company_name.data, form_clients.email.data, form_clients.phone_numb.data)
        print (text)
        crm_update_message(text)
        return flask.redirect(flask.url_for('index'))

    form_agreements = AgreementInputForm()
    if form_agreements.validate_on_submit():
        agreement = Agreements(
            company_1_id=form_agreements.client_1.data,
            company_2_id=form_agreements.client_2.data,
            agreement_num=form_agreements.agreement.data,
            cash_volume=form_agreements.trade_volume.data
        )
        print(1111)
        db_session.add(agreement)
        db_session.commit()
        flask.flash('DONE!')
        return flask.redirect(flask.url_for('index'))

    # В переменной current_user будет текущий пользователь
    # Если пользователь не залогинен, то current_user будет "анонимным"
    # првоерить можно так:

    # if current_user.is_anonymous:
    #     return 'NOOOOOOOOOOOOOO'

    # Но я этот код закоментил, т.к. выше стоит декоратор @login_required
    # а значит анонимный пользователь сюда не попадет
    # return 'Hello, {}'.format(current_user.email)
    return flask.render_template('welcome.html', form=form_clients,
                                 form_agreements=form_agreements,
                                 user=current_user, methods=['GET', 'POST'])


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        user = db_session.query(User).filter_by(email=form.email.data).first()

        if user is not None:
            if user.check_password(form.password.data):

                # Эта функция будет создавать сессию для пользователя
                # и проставляться cookie с ключом сессии
                login_user(user)

                next_url = flask.request.args.get('next', flask.url_for('index'))
                return flask.redirect(next_url)

        # Это механизм для вывода дополнительных сообщений на страницу
        # в файле login.html смотри <!-- Message flashing -->
        # подробнее тут http://flask.pocoo.org/docs/0.12/patterns/flashing/
        flask.flash('Email or password is wrong.')

    return flask.render_template('welcome_example.html', form=form)


@app.route('/users/')
def users():
    user_list = db_session.query(User).limit(10)
    return flask.render_template('users.html', user_list=user_list)


@app.route('/clients/')
def clients():
    company_list = db_session.query(Company).limit(10)
    return flask.render_template('clients.html', company_list=company_list)


@app.route('/agreements/')
def agreements():
    agreement_list = db_session.query(Agreements).limit(10)
    return flask.render_template('agreements.html', agreement_list=agreement_list)


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    logout_user()
    return flask.redirect(flask.url_for('login'))


@app.route('/telegram_inform/', methods=['POST'])
def telegram_inform():
    # TODO: выслать сообщение в телеграм
    send_message_template = "https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={client_update}"
    requests.get(send_message_template.format(**{
        "TOKEN":TELE_TOKEN,
        "chat_id":CRM_CHANNEL,
        "client_update":flask.request.form.get('message'),
    }))

    return flask.redirect(flask.url_for('index'))


if __name__ == '__main__':

    # # Это для создания базы с тестовым пользователем
    # Base.metadata.create_all(bind=engine)
    # u = User(email='no@any.mail')
    # u.password = '123'
    # db_session.add(u)
    # db_session.commit()

    app.run(port=5010, debug=True)
