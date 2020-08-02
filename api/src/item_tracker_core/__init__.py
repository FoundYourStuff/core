import boto3
import connexion

connexion_app = connexion.App(__name__)
DB = boto3.resource('dynamodb')

from item_tracker_core import handlers