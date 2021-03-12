import os

import connexion
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import User,Tag

if not os.getenv('DATABASE_URL'):
    os.environ['DATABASE_URL'] = os.popen("heroku config:get DATABASE_URL -a found-your-stuff-api").read().strip() #seems jank
DATABASE_URL = os.getenv('DATABASE_URL')
db = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=db)
session = Session()

def getUserByExternalID(external_id):
    currentTag = session.query(Tag).filter(Tag.external_id==external_id).first()
    user = session.query(User).get(currentTag.user_id)
    return {"phone":user.phone_number,
            "email":user.email}

def createNewUser(body):
    user = User(email=body['email'],
                    name=body['name'],
                    password=body['password'],
                    phone_number=body['phone_number'],
                    active=body['active'],
                    contact=body['contact'])
    session.add(user)
    session.commit()
    return {"id":user.id,
            "email":user.email,
            "name":user.name,
            "phone_number":user.phone_number,
            "contact":user.contact,
            "active":user.active}

def getUserByGuid(user_guid):
    user = session.query(User).filter(User.id==user_guid).first()
    return {"id":user.id,
            "email":user.email,
            "name":user.name,
            "phone_number":user.phone_number,
            "contact":user.contact,
            "active":user.active}

def updateUserByGuid(body, user_guid):
    user = session.query(User).filter(User.id==user_guid).first()
    #dangerous?
    for attribute in body:
        setattr(user, attribute, body[attribute])
    session.commit()
    return {"id":user.id,
            "email":user.email,
            "name":user.name,
            "phone_number":user.phone_number,
            "contact":user.contact,
            "active":user.active}

def createNewTag(body, user_guid):
    tag = Tag(user_id=user_guid,
                name=body['name'],
                picture=body['picture'],
                active=body['active'])
    session.add(tag)
    session.commit()
    return {"id":tag.id,
            "external_id":tag.external_id,
            "name":tag.name,
            "picture":tag.picture}

def getTagByGuid(tag_guid):
    tag = session.query(Tag).filter(Tag.id==tag_guid).first()
    return {"id":tag.id,
            "external_id":tag.external_id,
            "name":tag.name,
            "picture":tag.picture}

def updateTagByGuid(body, tag_guid):
    tag = session.query(Tag).filter(Tag.id==tag_guid).first()
    #dangerous?
    for attribute in body:
        setattr(tag, attribute, body[attribute])
    session.commit()
    return {"id":tag.id,
            "external_id":tag.external_id,
            "name":tag.name,
            "picture":tag.picture}
    

def getAllUsersTags(user_guid):
    tags = session.query(Tag).filter(Tag.user_id==user_guid).all()
    listOfTags = []
    for tag in tags:
         listOfTags.append({"id":tag.id,"external_id":tag.external_id,"name":tag.name,"picture":tag.picture})
    return listOfTags
