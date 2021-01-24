import os
import psycopg2
from sqlalchemy import create_engine, Table, Column, String, MetaData, Integer, Boolean, Sequence, BigInteger, LargeBinary, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base


#$Env:DATABASE_URL = $(heroku config:get DATABASE_URL -a found-your-stuff-api);  py.exe handlers.py

if os.getenv('DATABASE_URL') is None:
    os.environ['DATABASE_URL'] = os.popen("heroku config:get DATABASE_URL -a found-your-stuff-api").read().strip() #seems jank
DATABASE_URL = os.environ['DATABASE_URL']
db = create_engine(DATABASE_URL, echo=True)

meta = MetaData()
users = Table('users', meta,
                    Column('id', Integer, primary_key=True),
                    Column('email', String, nullable=False),
                    Column('password', String, nullable=False),
                    Column('name', String),
                    Column('phone_number', BigInteger),
                    Column('contact', Boolean, nullable=False),
                    Column('active', Boolean, nullable=False))

tags = Table('tags', meta,
                    Column('id', Integer, primary_key=True),
                    Column('user_id',Integer, ForeignKey("users.id"), nullable=False),
                    Column('name', String),
                    Column('picture', LargeBinary)
                    Column('active', Boolean, nullable=False))

messages = Table('messages', meta,
                    Column('id', BigInteger, primary_key=True),
                    Column('tag_id',Integer, ForeignKey("tags.id"), nullable=False),
                    Column('time_stamp', DateTime, nullable=False),
                    Column('body', String, nullable=False),
                    Column('picture', LargeBinary),
                    Column('read', Boolean, nullable=False))

meta.create_all(db)
# db.execute("INSERT INTO users (email, password, phone_number, contact, name, active) VALUES ('abc@gmail.com', 'abc', 1234, true, 'salvador dali', false)")

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
