from os import environ
from uuid import uuid4
from item_tracker_core import connexion_app, DB


def get_user_data(item_tag):
    tag_table = DB.Table(environ['TAG_TABLE'])
    user_table = DB.Table(environ['USER_TABLE'])
    tag_record = tag_table.get_item(
        Key={
            'item_tag': item_tag 
        },
        AttributesToGet=[
        'user_id',
        'item_desc',
        'item_name'
        ]
    )
    user_id = tag_record['Item']['user_id']
    user_record = user_table.get_item(
        Key={
            'user_id': user_id 
        },
        AttributesToGet=[
        'phone',
        'email',
        'name'
        ]
    )
    return {'user_record': user_record['Item'], 'tag_record': tag_record['Item']}



def add_tag(item_name, item_desc):
    tag_table = DB.Table(environ['TAG_TABLE'])
    item_tag = uuid4()
    new_tag = {
        'item_tag': item_tag,
        'user_id': 'bill',
        'item_name': item_name,
        'item_desc': item_desc
    }

    tag_table.put_item(new_tag)
    
    return {
        'item_tag': item_tag
    }

connexion_app.add_api('openapi.yml')
