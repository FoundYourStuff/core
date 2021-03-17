import os

import connexion
from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import sessionmaker

from models import User,Tag

if not os.getenv('DATABASE_URL'):
    os.environ['DATABASE_URL'] = os.popen("heroku config:get DATABASE_URL -a found-your-stuff-api").read().strip() #seems jank
DATABASE_URL = os.getenv('DATABASE_URL')
db = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=db)

def getUserByExternalID(external_id):
    session = Session()
    currentTag = session.query(Tag).filter(Tag.external_id==external_id).first()
    if currentTag is not None:
        user = session.query(User).filter(currentTag.user_id==User.id).first()
    session.close()
    if currentTag is not None and user is not None:
        return {"phone":user.phone_number,"email":user.email}
    else: 
        return {}, 404

    

def createNewUser(body):
    session = Session()
    user = User(email=body['email'],
                    name=body['name'],
                    password=body['password'],
                    phone_number=body['phone_number'],
                    active=body['active'],
                    contact=body['contact'])
    session.add(user)
    try:
        session.commit()
    except:
        session.rollback()
    #TODO: unit tests to make sure this is working properly
    return {"id":user.id,
            "email":user.email,
            "name":user.name,
            "phone_number":user.phone_number,
            "contact":user.contact,
            "active":user.active}

def getUserByGuid(user_guid):
    session = Session()
    user = session.query(User).filter(User.id==user_guid).first()
    session.close()
    if user is not None:
        return {"id":user.id,
                "email":user.email,
                "name":user.name,
                "phone_number":user.phone_number,
                "contact":user.contact,
                "active":user.active}
    else:
        return {}, 404

def updateUserByGuid(body, user_guid):
    session = Session()
    user = session.query(User).filter(User.id==user_guid).first()
    #dangerous?
    for attribute in body:
        setattr(user, attribute, body[attribute])
    try:
        session.commit()
    except:
        session.rollback()
    #TODO: unit tests to make sure this is working properly
    return {"id":user.id,
            "email":user.email,
            "name":user.name,
            "phone_number":user.phone_number,
            "contact":user.contact,
            "active":user.active}

def createNewTag(body, user_guid):
    session = Session()
    tag = Tag(user_id=user_guid,
                name=body['name'],
                picture=body['picture'],
                active=body['active'])
    session.add(tag)
    try:
        session.commit()
    except:
        session.rollback()
    #TODO: unit tests to make sure this is working properly
    return {"id":tag.id,
            "external_id":tag.external_id,
            "name":tag.name,
            "picture":tag.picture}

def getTagByGuid(tag_guid):
    session = Session()
    tag = session.query(Tag).filter(Tag.id==tag_guid).first()
    session.close()
    if tag is not None:
        return {"id":tag.id,
                "external_id":tag.external_id,
                "name":tag.name,
                "picture":tag.picture}
    else:
        return {}, 404

def updateTagByGuid(body, tag_guid):
    session = Session()
    tag = session.query(Tag).filter(Tag.id==tag_guid).first()
    #dangerous?
    for attribute in body:
        setattr(tag, attribute, body[attribute])
    try:
        session.commit()
    except:
        session.rollback()
    #TODO: unit tests to make sure this is working properly
    return {"id":tag.id,
            "external_id":tag.external_id,
            "name":tag.name,
            "picture":tag.picture}
    

def getAllUsersTags(user_guid):
    session = Session()
    tags = session.query(Tag).filter(Tag.user_id==user_guid).all()
    session.close()
    if tags is not None:
        listOfTags = []
        for tag in tags:
            listOfTags.append({"id":tag.id,"external_id":tag.external_id,"name":tag.name,"picture":tag.picture})
        return listOfTags
    else:
        return {}, 404
