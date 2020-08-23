import serverless_wsgi

from item_tracker_core import connexion_app


serverless_wsgi.TEXT_MIME_TYPES.append('application/problem+json')


def handler(event, context):
    return serverless_wsgi.handle_request(connexion_app.app, event, context)