import flask
import logging
from database import db_session, User, Company

app = flask.Flask(__name__)

app.config.update(SECRET_KEY='not very secret')

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='app.log'
                    )

from flask_login import LoginManager

login_manager = LoginManager()
login_manager.init_app(app)
# Это нужно для того, чтобы модуль
# login_manager знал куда редиректить пользователя
login_manager.login_view = 'login'


# Требуется для работы модуля flask_login
@login_manager.user_loader
def load_user(email):
    return db_session.query(User).filter(User.email == email).first()


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

    def __init__(self):
        super(AgreementInputForm, self).__init__()
        self.client_1.choices = db_session.query(
            Company.id, Company.company_name
        ).order_by(Company.company_name).all()
        self.client_2.choices = self.client_1.choices

    client_1 = wtforms.SelectField("Client 1")
    client_2 = wtforms.SelectField("Client 2")
    # StringField(
    #     validators=[validators.DataRequired()],
    #     description='Client 1 name')

    
    agreement = wtforms.StringField(
        validators=[validators.DataRequired(), validators.Email()],
        description='Agreement number')

    trade_volume = wtforms.PasswordField(
        validators=[validators.DataRequired()],
        description='Trade volume')


from flask_login import login_user, logout_user, login_required, current_user


@app.route('/', methods=['GET', 'POST'])
@login_required  # Если пользователь не залогинен,
                 # то редирект на страницу логина
def index():

    form_users = UserInputForm()
    # if form_users.validate_on_submit():
    #     client = User(telegram_id=form_clients.company_name.data,
    #                      itin_num=form_clients.itin_num.data,
    #                      email=form_clients.email.data,
    #                      phone_numb=form_clients.phone_numb.data)
    #     db_session.add(client)
    #     db_session.commit()
    #     flask.flash('DONE!')
    #     return flask.redirect(flask.url_for('index'))
    form_clients = ClientInputForm()
    if form_clients.validate_on_submit():
        client = Company(company_name=form_clients.company_name.data,
                         itin_num=form_clients.itin_num.data,
                         email=form_clients.email.data,
                         phone_numb=form_clients.phone_numb.data)
        db_session.add(client)
        db_session.commit()
        flask.flash('DONE!')
        return flask.redirect(flask.url_for('index'))
    form_agreements = AgreementInputForm()

    # В переменной current_user будет текущий пользователь
    # Если пользователь не залогинен, то current_user будет "анонимным"
    # првоерить можно так:

    # if current_user.is_anonymous:
    #     return 'NOOOOOOOOOOOOOO'

    # Но я этот код закоментил, т.к. выше стоит декоратор @login_required
    # а значит анонимный пользователь сюда не попадет
    # return 'Hello, {}'.format(current_user.email)
    return flask.render_template('welcome.html', form_clients=form_clients,
                                 form_agreements=form_agreements,
                                 methods=['GET', 'POST'])


@app.route('/clients/')
def clients():
    # form = ...
    # if form.validate_on_submit():
    company_list = db_session.query(Company).limit(10)
    return flask.render_template('clients.html', company_list=company_list)


# Выше мы указали этот view для login_manager'а:
# login_manager.login_view = 'login'
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

                next_url = flask.request.args.get(
                    'next', flask.url_for('index'))
                next_url = flask.url_for('index')
                return flask.redirect(next_url)

        # Это механизм для вывода дополнительных сообщений на страницу
        # в файле login.html смотри <!-- Message flashing -->
        # подробнее тут http://flask.pocoo.org/docs/0.12/patterns/flashing/
        flask.flash('Email or password is wrong.')

    return flask.render_template('login.html',
                                 form=form, methods=['GET', 'POST'])


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    logout_user()
    return flask.redirect(flask.url_for('login'))


if __name__ == '__main__':

    app.run(port=5120, debug=True)
