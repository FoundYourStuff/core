import os

import connexion

app = connexion.App(__name__, specification_dir='./')

app.add_api('openapi.yml')
ENV = os.getenv('FYS_WORKING_ENV')
if ENV:
    if ENV.lower() == 'dev':
        os.environ['FLASK_ENV'] = 'development'
        app.run(port=8080, debug=True)
