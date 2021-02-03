import os
import psycopg2
import uuid
import connexion
from sqlalchemy import create_engine, Table, Column, String, MetaData, Integer, Boolean, Sequence, BigInteger, LargeBinary, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID


#$Env:DATABASE_URL = $(heroku config:get DATABASE_URL -a found-your-stuff-api);  py.exe handlers.py

if os.getenv('DATABASE_URL') is None:
    os.environ['DATABASE_URL'] = os.popen("heroku config:get DATABASE_URL -a found-your-stuff-api").read().strip() #seems jank
DATABASE_URL = os.environ['DATABASE_URL']
db = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=db)
session = Session()
Base = declarative_base()
app = connexion.App(__name__, specification_dir='./')


class User(Base):
    __tablename__='users'
    id = Column('id', Integer, primary_key=True)
    email = Column('email', String, nullable=False)
    password = Column('password', String, nullable=False)
    name = Column('name', String)
    phone_number = Column('phone_number', BigInteger)
    contact = Column('contact', Boolean, nullable=False)
    active = Column('active', Boolean, nullable=False)

class Tag(Base):
    __tablename__="tags"
    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id',Integer, ForeignKey("users.id"), nullable=False)
    external_id = Column('external_id', UUID, nullable=False, default=uuid.uuid4, unique=True)
    name = Column('name', String)
    picture = Column('picture', LargeBinary)
    active = Column('active', Boolean, nullable=False)

class Message(Base):
    __tablename__="messages"
    id = Column('id', BigInteger, primary_key=True)
    tag_id = Column('tag_id',Integer, ForeignKey("tags.id"), nullable=False)
    time_stamp = Column('time_stamp', DateTime, nullable=False)
    body = Column('body', String, nullable=False)
    picture = Column('picture', LargeBinary)
    read = Column('read', Boolean, nullable=False)

def createTables():
    Base.metadata.create_all(db)



def getUserByExternalID(external_id):
    currentTag = session.query(Tag).get(external_id)
    user = session.query(User).get(currentTag.user_id)
    print(user.name)
    return {"phone":user.phone_number,
            "email":user.email}

app.add_api('openapi.yml')
# app.run(port=8080)
#createTables()
# getUserByTagId(1)