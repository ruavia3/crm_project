import flask

app = flask.Flask(__name__)

app.config.update(SECRET_KEY='not very secret')


import hashlib
import uuid
import sqlalchemy as sa
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin

engine = sa.create_engine('sqlite:///users.sqlite')
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
_password = 'empty'

class User(Base, UserMixin):  # UserMixin нужен для работы модуля flask_login
    __tablename__ = 'users'


    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.String)
    last_name = sa.Column(sa.String)
    email = sa.Column(sa.String, unique=True)
    _password = sa.Column(sa.String)

    def __init__(self, first_name=None, last_name=None, email=None, password=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User {} {} {}>'.format(self.first_name, self.last_name, self.email)

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext):
        
        self._password = '[' + plaintext + ']'
        
        # Генерируем соль
        
        #salt = uuid.uuid4().hex
        # Соединяем с паролем и получаем хеш
        #hashed_password = hashlib.sha512((plaintext + salt).encode()).hexdigest()
        # Сохраняем его вместе с сеолью в поле таблицы
        #self._password = salt + '|' + hashed_password

    def check_password(self, plaintext):
        # Получаем из поля "пароль" соль и хеш (хеш от пароля + соль)
        salt, hashed_password = self.password.split('|')
        # Проверяем соответствует ли сохраненный хаш от того, который мы получим с присланным паролем
        return hashed_password == hashlib.sha512((plaintext + salt).encode()).hexdigest()

    def get_id(self):  # Требуется для работы модуля flask_login
        return self.email


from flask_login import LoginManager

login_manager = LoginManager()
login_manager.init_app(app)
# Это нужно для того, чтобы модуль login_manager знал куда редиректить пользователя
login_manager.login_view = 'login'


# Требуется для работы модуля flask_login
@login_manager.user_loader
def load_user(email):
    return db_session.query(User).filter(User.email == email).first()


from flask_wtf import Form
import wtforms
from wtforms import validators


class LoginForm(Form):

    email = wtforms.StringField(
        validators=[validators.DataRequired(), validators.Email()],
        description='Email address')

    password = wtforms.PasswordField(
        validators=[validators.DataRequired()],
        description='Password')


from flask_login import login_user, logout_user, login_required, current_user
from flask import Flask, render_template, request

@app.route('/')
def home():
    return render_template('welcome.html')
@login_required  # Если пользователь не залогинен, то редирект на страницу логина

def index():
    # В переменной current_user будет текущий пользователь
    # Если пользователь не залогинен, то current_user будет "анонимным"
    # првоерить можно так:

    # if current_user.is_anonymous:
    #     return 'NOOOOOOOOOOOOOO'

    # Но я этот код закоментил, т.к. выше стоит декоратор @login_required
    # а значит анонимный пользователь сюда не попадет
    return 'Hello, {}'.format(current_user.email)


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

                next_url = flask.request.args.get('next', flask.url_for('index'))
                return flask.redirect(next_url)

        # Это механизм для вывода дополнительных сообщений на страницу
        # в файле login.html смотри <!-- Message flashing -->
        # подробнее тут http://flask.pocoo.org/docs/0.12/patterns/flashing/
        flask.flash('Email or password is wrong.')

    return flask.render_template('login.html', form=form, user=current_user)


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    logout_user()
    return flask.redirect(flask.url_for('login'))


if __name__ == '__main__':

    # # Это для создания базы с тестовым пользователем
    Base.metadata.create_all(bind=engine)
    u = User(email='test@gmail.com')
    u.password = '123'
    db_session.add(u)
    db_session.commit()

    app.run(port=5010, debug=True)