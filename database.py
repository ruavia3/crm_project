
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///crm_project_db.sqlite')

db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(120), unique=True)
    telegram_id = Column(String(50), unique=True)

    def __init__(self, first_name=None, last_name=None, email=None, telegram_id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.telegram_id = telegram_id

    def __repr__(self):
        return '<User {} {} {}>'.format(self.first_name, self.last_name, self.email)


class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    conmany_name = Column(String(50))
    itin_num = Column(String(12))
    email = Column(String(120), unique=True)
    phone_numb = Column(String(50), unique=True)

    def __init__(self, conmany_name=None, itin_num=None, email=None, phone_numb=None):
        self.conmany_name = conmany_name
        self.itin_num = itin_num
        self.email = email
        self.phone_numb = phone_numb

    def __repr__(self):
        return '<Company {} {} {} {}>'.format(self.conmany_name, self.itin_num, self.email, self.phone_numb)

class Agreements(Base):
    __tablename__ = 'companies agreements'
    id = Column(Integer, primary_key=True)
    conmany_1_id = Column(Integer, ForeignKey('Company.id'))
    conmany_1_name = Column(String(50))
    conmany_2_id = Column(Integer, ForeignKey('Company.id'))
    conmany_2_name = Column(String(50))
    agreement_num = Column(String(12))
    cash_volume = Column(String(50))

    def __init__(self, conmany_1_name=None, conmany_2_name=None, agreement_num=None, cash_volume=None):
        self.conmany_1_name = conmany_1_name
        self.conmany_2_name = conmany_2_name
        self.agreement_num = agreement_num
        self.cash_volume = cash_volume

    def __repr__(self):
        return '<Agreement {} {} {} {}>'.format(self.agreement_num, self.conmany_1_name, self.conmany_2_name, self.cash_volume)

class client_requests(Base):
    __tablename__ = 'companies agreements'
    id = Column(Integer, primary_key=True)
    conmany_id = Column(Integer, ForeignKey('Company.id'))
    conmany_name = Column(String(50))
    request = Column(String(250))
    req_status = Column(String(50))

    def __init__(self, conmany_name=None, request=None, req_status=None):
        self.conmany_name = conmany_name
        self.request = request
        self.req_status = req_status

    def __repr__(self):
        return '<Request {} {} {}>'.format(self.conmany_name, self.request, self.req_status)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
