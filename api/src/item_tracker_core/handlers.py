import os
import psycopg2
from sqlalchemy import create_engine, Table, Column, String, MetaData, Integer, Boolean, Sequence, BigInteger, LargeBinary, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base


#$Env:DATABASE_URL = $(heroku config:get DATABASE_URL -a found-your-stuff-api);  py.exe handlers.py

if os.getenv('DATABASE_URL') is None:
    os.environ['DATABASE_URL'] = os.popen("heroku config:get DATABASE_URL -a found-your-stuff-api").read().strip() #seems jank
DATABASE_URL = os.environ['DATABASE_URL']
db = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()

class User(Base):
    __tablename__='users'
    id = Column('id', Integer, primary_key=True)
    email = Column('email', String, nullable=False)
    password = Column('password', String, nullable=False)
    name = Column('name', String)
    phoneNumber = Column('phone_number', BigInteger)
    contact = Column('contact', Boolean, nullable=False)
    active = Column('active', Boolean, nullable=False)

class Tag(Base):
    __tablename__="tags"
    id = Column('id', Integer, primary_key=True)
    userID = Column('user_id',Integer, ForeignKey("users.id"), nullable=False)
    name = Column('name', String)
    picture = Column('picture', LargeBinary)
    active = Column('active', Boolean, nullable=False)

class Message(Base):
    __tablename__="messages"
    id = Column('id', BigInteger, primary_key=True)
    tagID = Column('tag_id',Integer, ForeignKey("tags.id"), nullable=False)
    timeStamp = Column('time_stamp', DateTime, nullable=False)
    body = Column('body', String, nullable=False)
    picture = Column('picture', LargeBinary)
    read = Column('read', Boolean, nullable=False)

def createTables():
    Base.metadata.create_all(db)

createTables()