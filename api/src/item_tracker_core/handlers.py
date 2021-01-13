import os 
import psycopg2
import sqlalchemy


#$Env:DATABASE_URL = $(heroku config:get DATABASE_URL -a found-your-stuff-api);  py.exe handlers.py
os.environ['DATABASE_URL'] = os.popen("heroku config:get DATABASE_URL -a found-your-stuff-api").read().strip() #seems jank
print(os.environ['DATABASE_URL'])
DATABASE_URL = os.environ['DATABASE_URL']
db = sqlalchemy.create_engine(DATABASE_URL)
db.execute("INSERT INTO users (email, password, phone_number, contact, name, active) VALUES ('abc@gmail.com', 'abc', 1234, true, 'salvador dali', false)")

# conn = None
# try:
#     conn = psycopg2.connect(DATABASE_URL)
#     cur = conn.cursor()
#     print('PostgreSQL database version:')
#     cur.execute('SELECT version()')
#     db_version = cur.fetchone()
#     print(db_version)
#     cur.close()
# except Exception as error:
#     print('Cause: {}'.format(error))

# finally:
#     if conn is not None:
#         conn.close()
#         print('Closed DB')


