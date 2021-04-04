import os

import connexion
from flask_cors import CORS

app = connexion.App(__name__, specification_dir='./')
cors = CORS(app.app)

app.add_api('openapi.yml')
ENV = os.getenv('FYS_WORKING_ENV')
if ENV:
    if ENV.lower() == 'dev':
        os.environ['FLASK_ENV'] = 'development'
        app.run(port=8080, debug=True)
