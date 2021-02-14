import os
import psycopg2
import uuid
import connexion
from sqlalchemy import create_engine, Table, Column, String, MetaData, Integer, Boolean, Sequence, BigInteger, ForeignKey, DateTime
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

def createTables():
    Base.metadata.create_all(db)



def getUserByExternalID(external_id):
    currentTag = session.query(Tag).filter(Tag.external_id==external_id).first()
    user = session.query(User).get(currentTag.user_id)
    return {"phone":user.phone_number,
            "email":user.email}

def createNewUser(body):
    newUser = User(email=body['email'],
                    name=body['name'],
                    password=body['password'],
                    phone_number=body['phone_number'],
                    active=body['active'],
                    contact=body['contact'])
    session.add(newUser)
    session.commit()

def getUserByGuid(user_guid):
    user = session.query(User).filter(User.id==user_guid).first()
    return {"email":user.email,
            "password":user.password,
            "name":user.name,
            "phone_number":user.phone_number,
            "contact":user.contact,
            "active":user.active}

def updateUserByGuid(body, user_guid):
    print("hello")
    session.query(User).filter(User.id==user_guid).update({"email":body['email'], "name":body['name'], "password":body['password'],
                                                                    "phone_number":body['phone_number'], "active":body['active'], 
                                                                    "contact":body['contact']})
    session.commit()

def createNewTag(body, user_guid):
    newTag = Tag(user_id=user_guid,
                    name=body['name'],
                    picture=body['picture'],
                    active=body['active'])
    session.add(newTag)
    session.commit()

app.add_api('openapi.yml')
#app.run(port=8080, debug=True)