import os
import connexion
import psycopg2
import uuid
from sqlalchemy import Table, Column, String, MetaData, Integer, Boolean, Sequence, BigInteger, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID


#$Env:DATABASE_URL = $(heroku config:get DATABASE_URL -a found-your-stuff-api);  py.exe handlers.py

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
    external_id = Column('external_id', UUID(as_uuid=True), nullable=False, default=uuid.uuid4, unique=True)
    name = Column('name', String)
    picture = Column('picture', String)
    active = Column('active', Boolean, nullable=False)

class Message(Base):
    __tablename__="messages"
    id = Column('id', BigInteger, primary_key=True)
    tag_id = Column('tag_id',Integer, ForeignKey("tags.id"), nullable=False)
    time_stamp = Column('time_stamp', DateTime, nullable=False)
    body = Column('body', String, nullable=False)
    picture = Column('picture', String)
    read = Column('read', Boolean, nullable=False)
