from os import environ
from uuid import uuid4
from item_tracker_core import connexion_app, DB


def getUserData(itemTag):
    tagTable = DB.Table(environ['TAG_TABLE'])
    userTable = DB.Table(environ['USER_TABLE'])
    tagRecord = tagTable.getItem(
        Key={
            'item_tag': itemTag 
        },
        AttributesToGet=[
        'user_id',
        'item_desc',
        'item_name'
        ]
    )
    userId = tagRecord['Item']['user_id']
    userRecord = userTable.getItem(
        Key={
            'user_id': userId 
        },
        AttributesToGet=[
        'phone',
        'email',
        'name'
        ]
    )
    return {'user_record': userRecord['Item'], 'tag_record': tagRecord['Item']}



def addTag(body):
    tagTable = DB.Table(environ['TAG_TABLE'])
    itemTag = str(uuid4())
    newTag = {
        'item_tag': itemTag,
        'user_id': 'bill',
        'item_name': body['item_name'],
        'item_desc': body['item_desc']
    }

    tagTable.putItem(Item=newTag)
    
    return {
        'item_tag': itemTag
    }

connexion_app.add_api('openapi.yml')
