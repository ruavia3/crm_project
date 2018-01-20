import flask
from database import db_session, User, Company

app = flask.Flask(__name__)

app.config.update(SECRET_KEY='not very secret')

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


@app.route('/')
@login_required  # Если пользователь не залогинен,
                 # то редирект на страницу логина
def index():
    # В переменной current_user будет текущий пользователь
    # Если пользователь не залогинен, то current_user будет "анонимным"
    # првоерить можно так:

    # if current_user.is_anonymous:
    #     return 'NOOOOOOOOOOOOOO'

    # Но я этот код закоментил, т.к. выше стоит декоратор @login_required
    # а значит анонимный пользователь сюда не попадет
    # return 'Hello, {}'.format(current_user.email)
    return flask.render_template('welcome.html')

@app.route('/clients/')
def clients():
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

    return flask.render_template('login.html', form=form)


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    logout_user()
    return flask.redirect(flask.url_for('login'))


if __name__ == '__main__':

    app.run(port=5120, debug=True)
