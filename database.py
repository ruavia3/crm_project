
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from flask_login import UserMixin

from settings import DB_NAME  # импорт настройки - название базы данных
import hashlib
import uuid

engine = create_engine(DB_NAME)
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class User(Base, UserMixin):  # таблица пользователей системы (они заводят
                    # клиентов и могут выгружать отчеты)
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(120), unique=True)
    telegram_id = Column(String(50), unique=True)
    _password = Column(String(50), name='password')

    def __init__(self, first_name=None, last_name=None,
                 email=None, telegram_id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.telegram_id = telegram_id

    def __repr__(self):
        return '<User {} {} {}>'.format(self.first_name,
                                        self.last_name, self.email)

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext):
        # Генерируем соль
        salt = uuid.uuid4().hex
        # Соединяем с паролем и получаем хеш
        hashed_password = hashlib.sha512(
            (plaintext + salt).encode()).hexdigest()
        # Сохраняем его вместе с сеолью в поле таблицы
        self._password = salt + '|' + hashed_password

    def check_password(self, plaintext):
        # Получаем из поля "пароль" соль и хеш (хеш от пароля + соль)
        salt, hashed_password = self.password.split('|')
        # Проверяем соответствует ли сохраненный хаш от того,
        # который мы получим с присланным паролем
        return hashed_password == hashlib.sha512(
            (plaintext + salt).encode()).hexdigest()

    def get_id(self):  # Требуется для работы модуля flask_login
        return self.email


class Company(Base):  # таблица компаний-клиентов,
                    # которая содержить основные данные клиентов
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    company_name = Column(String(50))  # наименование компании
    itin_num = Column(String(12))  # ИНН
    email = Column(String(120), unique=True)  # эл.почта компании
    phone_numb = Column(String(50), unique=True)  # телефон

    def __init__(
            self, company_name=None, itin_num=None,
            email=None, phone_numb=None):
        self.company_name = company_name
        self.itin_num = itin_num
        self.email = email
        self.phone_numb = phone_numb

    def __repr__(self):
        return '<Company {} {} {} {}>'.format(
            self.company_name, self.itin_num,
            self.email, self.phone_numb)


class Agreements(Base):  # таблица соглашений между двумя клиентами (данные
                        # должны поддтягиваться из таблицы компании и вручную
                        # заносятся данные об обороте между клиентами и
                        # и номер соглашения)
    __tablename__ = 'companies_agreements'
    id = Column(Integer, primary_key=True)
    company_1_id = Column(Integer, ForeignKey('companies.id'))
    company_1 = relationship('Company', foreign_keys=[company_1_id])
    # conmany_1_name = Column(String(50), ForeignKey('Company.conmany_name'))
    company_2_id = Column(Integer, ForeignKey('companies.id'))
    company_2 = relationship('Company', foreign_keys=[company_2_id])
    agreement_num = Column(String(12))
    cash_volume = Column(String(50))

    def __repr__(self):
        return '<Agreement {} {} {} {}>'.format(
            self.agreement_num, self.company_1.name,
            self.company_2.name, self.cash_volume)


class ClientRequests(Base):  # таблица запросов и проблем
                            # клиентов которые предстоит решить)
    __tablename__ = 'companies_requests'
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'))
    company_name = relationship('Company', foreign_keys=[company_id])
    request = Column(String(250))
    req_status = Column(String(50))

    def __init__(self, company_name=None, request=None, req_status=None):
        self.company_name = company_name
        self.request = request
        self.req_status = req_status

    def __repr__(self):
        return '<Request {} {} {}>'.format(
            self.company_name, self.request, self.req_status)


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    # u = User(email='no@any.mail')
    # u.password = '123'
    # db_session.add(u)
    # db_session.commit()
    # # Это для создания базы с тестовым пользователем
